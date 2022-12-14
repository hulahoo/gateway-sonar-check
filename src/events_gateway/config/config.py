from pydantic import BaseSettings


class Settings(BaseSettings):

    EVENTS_PORT: int = 8000
    EVENTS_HOST: str = "0.0.0.0"
    KAFKA_SERVER: str = "kafka:9092"
    COLLECTOR_TOPIC: str = "collector"

    # test
    SYSLOG_HOST_TO_CONNECT: str = "localhost"

    class Config:
        env_file = "./.env"


settings = Settings()
