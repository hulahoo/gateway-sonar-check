from pydantic import BaseSettings


class Settings(BaseSettings):

    EVENTS_PORT: int = 9000
    EVENTS_HOST: str = "localhost"
    KAFKA_SERVER: str = "localhost"
    COLLECTOR_TOPIC: str = "collector"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_USER: str = "username"
    POSTGRES_DB: str = "db"
    POSTGRES_PORT: int = 5432

    class Config:
        env_file = "./.env"


settings = Settings()
