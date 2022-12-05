from pydantic import BaseSettings


class Settings(BaseSettings):

    EVENTS_PORT: int = 9000
    EVENTS_HOST: str = "gateway"
    KAFKA_SERVER: str = "kafka:9092"
    COLLECTOR_TOPIC: str = "collector"

    # test
    SYSLOG_HOST_TO_CONNECT: str = "localhost"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_USER: str = "username"
    POSTGRES_DB: str = "db"
    POSTGRES_PORT: int = 5432

    class Config:
        env_file = "./.env"


settings = Settings()
