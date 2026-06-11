import logging
from xml.etree.ElementTree import Element, SubElement, tostring

from aiomqtt import Client

from src.core.configs import Settings
from src.services.database.models import CommandStatus

logger = logging.getLogger(__name__)


class MQTTPublisher:

    def __init__(self, client: Client, settings: Settings) -> None:
        self._client = client
        self._topic = settings.MQTT_TOPIC_FEEDBACK

    async def publish_done(self, request_id: str) -> None:
        """Publish success feedback"""
        await self._publish(request_id, CommandStatus.DONE)

    async def publish_error(self, request_id: str, message: str) -> None:
        """Publish failure with descritive message feedback"""
        await self._publish(request_id, CommandStatus.ERROR, message=message)

    async def _publish(
        self,
        request_id: str,
        status: CommandStatus,
        message: str | None = None,
    ) -> None:
        payload = self._build_xml(request_id, status, message)

        try:
            await self._client.publish(self._topic, payload=payload, qos=1)
            logger.info(
                "FEEDBACK published | request_id=%s status=%s topic=%s",
                request_id, status, self._topic,
            )
        except Exception as e:
            logger.error(
                "Error to publish feedback | request_id=%s erro=%s",
                request_id, e,
            )

    @staticmethod
    def _build_xml(
        request_id: str,
        status: CommandStatus,
        message: str | None = None,
    ) -> bytes:
        """
        Builds XML feedback payload according to ARQ-017:
        <camera_feedback>
            <request_id>automa_20260610143022847</request_id>
            <status>DONE</status>
            <!-- Only when ERROR: -->
            <message>...</message>
        </camera_feedback>
        """
        root = Element("camera_feedback")

        SubElement(root, "request_id").text = request_id
        SubElement(root, "status").text = status.value

        if message is not None:
            SubElement(root, "message").text = message

        return tostring(root, encoding="utf-8", xml_declaration=True)