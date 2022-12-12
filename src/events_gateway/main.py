import socketserver

from events_gateway.config.config import settings
from events_gateway.config.log_conf import logger
from events_gateway.apps.models.migrations import create_migrations
from events_gateway.apps.consumer.events_consumer import SyslogTCPHandler


def start_serve():
    with socketserver.TCPServer((settings.EVENTS_HOST, settings.EVENTS_PORT), SyslogTCPHandler) as server:
        logger.info("Start listening...")
        try:
            server.serve_forever(poll_interval=0.5)
        except Exception as e:
            logger.error(f"Error occured: {e}")


if __name__ == "__main__":
    create_migrations()
    start_serve()
