import socketserver
from typing import Dict, Any, Optional

from config.config import settings
from config.log_conf import logger
from apps.cron.job import CronModule
from apps.models.models import PatternStorage
from apps.producer.produce_message import producer_entrypoint
from apps.consumer.services import base_field_extractor, convert_to_dict
from apps.models.services import get_first_pattern, create_log_statistic


class SyslogTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def get_pattern(self) -> PatternStorage:
        return get_first_pattern()

    def initialize(self) -> None:
        logger.info("Initializing cron jobs...")
        cron = CronModule()
        cron.add_job(1, self.get_pattern)
        cron.start()

    def handle(self) -> None:
        if not hasattr(self, "pattern"):
            self.initialize()

        incoming_events = bytes.decode(self.request.recv(1024).strip())
        received_log_statistic = self.record_to_json(incoming_events=incoming_events)
        logger.info(f"Retrieved log statistic: {incoming_events}")
        if received_log_statistic is not None:
            try:
                create_log_statistic(statistic=received_log_statistic)
                self.send_incoming_event_to_kafka(incoming_events=received_log_statistic)
                logger.info(f"Data was sent to events collector. Data is: {received_log_statistic}")
            except Exception as e:
                logger.exception(f"Error occured: {e}")
                return

    @staticmethod
    def record_to_json(*, incoming_events: str) -> Optional[dict]:
        try:
            log = convert_to_dict(incoming_events=incoming_events)
            base_field_extractor(log)
            log_new = {"feed": log, 'link': log.get('link', log.get('URL', '')), 'type': log.get('type', 'json')}
            log_new['feed']['link'] = log_new.get('link')
            log_new['feed']['format_of_feed'] = log_new.get('type').upper()
            return log_new
        except Exception as e:
            logger.exception(f"Error occured while creating log: {e}")
            return

    def send_incoming_event_to_kafka(self, incoming_events: Dict[str, Any]):
        producer_entrypoint(message_to_send=incoming_events, topic=settings.COLLECTOR_TOPIC)
