import socketserver
from typing import Dict, Any, Optional

from events_gateway.config.config import settings
from events_gateway.config.log_conf import logger
from events_gateway.apps.consumer.services import convert_to_dict
from events_gateway.apps.consumer.selectors import stat_received_provider
from events_gateway.apps.producer.produce_message import producer_entrypoint


class SyslogTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self) -> None:
        incoming_events = bytes.decode(self.request)
        stat_received_provider.create()
        logger.info("Stat received increased")
        received_log_statistic = self.record_to_json(incoming_events=incoming_events)
        logger.info(f"Retrieved log statistic: {received_log_statistic}")
        if received_log_statistic is not None:
            try:
                self.send_incoming_event_to_kafka(incoming_events=received_log_statistic)
                logger.info(f"Data was sent to events collector. Data is: {received_log_statistic}")
            except Exception as e:
                logger.error(f"Error occured: {e}")
                return

    @staticmethod
    def record_to_json(*, incoming_events: str) -> Optional[dict]:
        try:
            log = convert_to_dict(incoming_events=incoming_events)
            log_new = {"feed": log, 'link': log.get('link', log.get('URL', '')), 'type': log.get('type', 'json')}
            log_new['feed']['link'] = log_new.get('link')
            log_new['feed']['format_of_feed'] = log_new.get('type').upper()
            return log_new
        except Exception as e:
            logger.error(f"Error occured while creating log: {e}")
            return

    def send_incoming_event_to_kafka(self, incoming_events: Dict[str, Any]):
        producer_entrypoint(message_to_send=incoming_events, topic=settings.EVENTS_COLLECTOR_TOPIC)
