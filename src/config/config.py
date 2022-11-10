from pydantic import BaseSettings


class Settings(BaseSettings):

    PORT: int = 9000
    HOST: str = "localhost"
    KAFKA_SERVER: str = "localhost"
    COLLECTOR_TOPIC: str = "collector"

    class Config:
        env_prefix = "EVENTS_"
        env_file = "./.env"


settings = Settings()
