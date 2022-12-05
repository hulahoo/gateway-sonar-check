import socketserver

from loguru import logger

from src.config.config import settings
from src.config.log_conf import conf
from src.apps.models.migrations import create_migrations
from src.apps.consumer.events_consumer import SyslogTCPHandler


def start_serve():
    with socketserver.TCPServer((settings.EVENTS_HOST, settings.EVENTS_PORT), SyslogTCPHandler) as server:
        logger.info("Start listening...")
        try:
            server.serve_forever(poll_interval=0.5)
        except Exception as e:
            logger.error(f"Error occured: {e}")


if __name__ == "__main__":
    logger.remove()
    logger.configure(**conf)

    create_migrations()
    start_serve()
