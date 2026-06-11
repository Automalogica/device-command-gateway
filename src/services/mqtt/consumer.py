import logging
from aiomqtt import Client, MqttError

from src.core.configs import Settings
from src.services.database import CommandCRUD
from src.tools.parser import BaseParser

logger = logging.getLogger(__name__)


class MQTTConsumer:
    def __init__(
        self,
        settings: Settings,
        crud: CommandCRUD,
        parser: BaseParser,
    ) -> None:
        self._settings = settings
        self._crud = crud
        self._parser = parser

    async def start(self) -> None:
        """Consumer loop starts - never returns when service active"""
        logger.info("Conectando ao broker %s:%s", self._settings.MQTT_HOST, self._settings.MQTT_PORT)

        async with Client(
            hostname=self._settings.MQTT_HOST,
            port=self._settings.MQTT_PORT,
            username=self._settings.mqtt_username,
            password=self._settings.mqtt_password,
        ) as client:
            await client.subscribe(self._settings.MQTT_TOPIC_COMMAND)
            logger.info("Readin from topic '%s' — waiting messages", self._settings.MQTT_TOPIC_COMMAND)

            async for message in client.messages:
                await self._handle(message)

    async def _handle(self, message) -> None:
        payload = bytes(message.payload)

        try:
            data = self._parser.parse(payload)
            self._validate(data)
        except ValueError as e:
            logger.warning("Invalid message ignored: %s | payload: %s", e, payload)
            return

        try:
            await self._crud.insert_command(
                request_id=data["request_id"],
                camera_id=data.get("camera_id", ""),
                command=data["command"],
                params=data.get("params"),
            )
            logger.info("Registered new command | request_id=%s command=%s", data["request_id"], data["command"])
        except Exception as e:
            logger.error("Error to persist command | request_id=%s erro=%s", data.get("request_id"), e)

    @staticmethod
    def _validate(data: dict) -> None:
        required = ("request_id", "command")
        missing = [field for field in required if not data.get(field)]
        if missing:
            raise ValueError(f"Required fields are missing: {missing}")