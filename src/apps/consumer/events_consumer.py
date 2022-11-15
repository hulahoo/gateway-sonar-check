import socketserver
from typing import Dict, Any

from loguru import logger

from src.config.config import settings
from src.apps.cron.job import CronModule
from src.apps.producer.produce_message import producer_entrypoint
from src.apps.consumer.services import log_text_to_json, base_field_extractor
from src.apps.models.services import get_first_pattern, create_log_statistic


class SyslogTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def get_pattern(self):
        return get_first_pattern()

    def cron(self):
        self.pattern = self.get_pattern()

    def initialize(self):
        self.pattern = self.get_pattern()
        cron = CronModule()
        cron.add_job(1, self.cron)
        cron.start()

    def handle(self) -> None:
        if not hasattr(self, "pattern"):
            self.initialize()

        incoming_events = bytes.decode(self.request.recv(1024).strip())
        received_log_statistic = self.record_to_json(incoming_events=incoming_events, pattern=self.pattern)
        if received_log_statistic is not None:
            try:
                create_log_statistic(statistic=received_log_statistic)
                self.send_incoming_event_to_kafka(incoming_events=incoming_events)
                logger.info(f"Data was sent. Data is: {received_log_statistic}")
            except Exception as e:
                logger.exception(f"Error occured: {e}")
                return

    @staticmethod
    def record_to_json(*, incoming_events: str, pattern: str):
        try:
            log = log_text_to_json(incoming_events, pattern)
            base_field_extractor(log)
            log_new = {"feed": log, 'link': log.get('link', log.get('URL', '')), 'type': log.get('type', 'json')}
            log_new['feed']['link'] = log_new.get('link')
            log_new['feed']['format_of_feed'] = log_new.get('type').upper()
            return log_new
        except Exception as e:
            logger.exception(f"Error occured while creating log: {e}")
            return None

    def send_incoming_event_to_kafka(self, incoming_events: Dict[str, Any]):
        producer_entrypoint(message_to_send=incoming_events, topic=settings.COLLECTOR_TOPIC)