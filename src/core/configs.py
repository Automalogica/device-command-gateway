import logging

from dotenv import find_dotenv, load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    def setup_logging(self, logging_level: str = "DEBUG"):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )

    ##### DATABASE #####
    POSTGRES_DB: str = Field(...,
                             description="Postgres database name",
                             examples=["device-command-gateway", "postgres"])
    POSTGRES_USER: str = Field(...,
                               description="Postgres username",
                               examples=["automa", "camera-agent", "postgres"])
    POSTGRES_PWD: str = Field(...,
                              description="Postgres password",
                              examples=["automa123", "123", "postgres"])
    ##### DATABASE #####

    ##### MQTT #####
    EMQX_DASHBOARD_PWD: str = Field(...,
                                    description="EMQX Dashboard password",
                                    examples=["emqx", "123", "automa"])
    MQTT_HOST: str = Field(...,
                           description="MQTT broker hostname",
                           examples=["emqx", "localhost", "192.168.1.10"])
    MQTT_PORT: int = Field(default=1883,
                           description="MQTT broker port",
                           examples=[1883])
    MQTT_USER: str = Field(...,
                           description="MQTT username",
                           examples=["automa", "camera-agent"])
    MQTT_PWD: str = Field(...,
                          description="MQTT password",
                          examples=["automa123", "123"])
    MQTT_TOPIC_COMMAND: str = Field(default="camera/command",
                                    description="Tópico de entrada de comandos",
                                    examples=["camera/command"])
    MQTT_TOPIC_FEEDBACK: str = Field(default="camera/feedback",
                                     description="Tópico de retorno ao SCADA",
                                     examples=["camera/feedback"])
    ##### MQTT #####

    ##### GENERAL #####
    WORKER_POOL_SIZE: int = Field(...,
                                  description="Max workers",
                                  examples=[1, 5, 10])
    TELNET_TIMEOUT_MS: int = Field(...,
                                   description="Telnet timeout ms",
                                   examples=[5000, 10000, 15000])
    TELNET_MAX_RETRIES: int = Field(...,
                                    description="Telnet max retries",
                                    examples=[1, 2, 3])
    ##### GENERAL #####


settings: Settings = Settings()
settings.setup_logging()