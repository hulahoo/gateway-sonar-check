import socketserver

from loguru import logger

from src.config.config import settings
from src.config.log_conf import conf
from src.apps.consumer.events_consumer import SyslogTCPHandler

if __name__ == "__main__":
    logger.remove()
    logger.configure(**conf)

    logger.info(f"{settings.__dict__}")
    with socketserver.TCPServer((settings.HOST, settings.PORT), SyslogTCPHandler) as server:
        logger.info("Start listening...")
        server.serve_forever()
