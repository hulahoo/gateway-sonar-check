from pydantic import BaseSettings


class Settings(BaseSettings):

    EVENTS_PORT: int = 8000
    EVENTS_HOST: str = "localhost"
    KAFKA_BOOTSTRAP_SERVER: str = "localhost"
    EVENTS_COLLECTOR_TOPIC: str = "syslog"
    CSRF_ENABLED: bool = True
    SESSION_COOKIE_SECURE: bool = True

    APP_POSTGRESQL_HOST: str = "localhost"
    APP_POSTGRESQL_PASSWORD: str = "password"
    APP_POSTGRESQL_USER: str = "username"
    APP_POSTGRESQL_NAME: str = "db"
    APP_POSTGRESQL_PORT: int = 5432

    class Config:
        env_file = "./.env"


settings = Settings()
