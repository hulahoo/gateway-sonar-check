from pydantic import BaseSettings


class Settings(BaseSettings):

    EVENTS_PORT: int = 8000
    EVENTS_HOST: str = "0.0.0.0"
    KAFKA_BOOTSTRAP_SERVER: str = "kafka:9092"
    EVENTS_COLLECTOR_TOPIC: str = "collector"

    APP_POSTGRESQL_HOST: str = "localhost"
    APP_POSTGRESQL_PASSWORD: str = "password"
    APP_POSTGRESQL_USER: str = "username"
    APP_POSTGRESQL_NAME: str = "db"
    APP_POSTGRESQL_PORT: int = 5432

    class Config:
        env_file = "./.env"


settings = Settings()
