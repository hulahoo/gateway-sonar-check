from typing import Union, List

from loguru import logger

from src.apps.services import benchmark
from src.apps.producer.abstract import BaseProducer


class MessageProducer(BaseProducer):

    def send_message(self, *, message_to_send: dict, topic: Union[List, str]):
        self._send_data(data=message_to_send, topic=topic, producer=self.producer)
        logger.info("Message successfully sent!")

    @benchmark
    def start_process(self):
        self.send_message(message_to_send=self.message_to_send, topic=self.topic)


def producer_entrypoint(*, message_to_send: dict, topic: str):
    producer = MessageProducer(message_to_send=message_to_send, topic=topic)
    logger.info("Producer created...")
    producer.start_process()
