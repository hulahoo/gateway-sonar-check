import socketserver
from typing import Dict, Any

from loguru import logger

from src.config.config import settings
from src.apps.producer.produce_message import producer_entrypoint


class SyslogTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self) -> None:
        incoming_events = bytes.decode(self.request.recv(1024).strip())
        logger.info(f"Recieved events: {incoming_events}")

        self.send_incoming_event_to_kafka(incoming_events=incoming_events)

    def send_incoming_event_to_kafka(self, incoming_events: Dict[str, Any]):
        producer_entrypoint(message_to_send=incoming_events, topic=settings.COLLECTOR_TOPIC)
