import threading
import socketserver

from events_gateway.config.config import settings
from events_gateway.config.log_conf import logger
from events_gateway.web.routers.api import execute as flask_app
from events_gateway.apps.consumer.events_consumer import SyslogTCPHandler


def start_serve():
    """
    Main function to start listening SYSLOG protocol
    """
    with socketserver.TCPServer((settings.EVENTS_HOST, settings.EVENTS_PORT), SyslogTCPHandler) as server:
        logger.info("Start listening...")
        try:
            server.serve_forever()
        except Exception as e:
            logger.error(f"Error occured: {e}")


def execute():
    """
    Function entrypoint to start:
    1. SYSLOG protocol app to receive data
    2. Flask application to serve enpoints
    3. Apply migrations
    """
    flask_thread = threading.Thread(target=flask_app)
    syslog_thread = threading.Thread(target=start_serve)

    logger.info("Start Flask app")
    flask_thread.start()

    logger.info("Start gateway")
    syslog_thread.start()
