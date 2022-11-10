import json
from abc import ABC, abstractmethod
from typing import List, Union

from loguru import logger
from kafka.producer import KafkaProducer

from src.config.config import settings


class AbstractProducer(ABC):
    """
    Абстрактный класс для базового описания продюсера
    """

    @abstractmethod
    def start_producer(self):
        raise NotImplementedError

    @abstractmethod
    def send_message(self):
        raise NotImplementedError

    @abstractmethod
    def start_process(self):
        raise NotImplementedError


class BaseProducer(AbstractProducer):

    @logger.catch
    def _send_data(
        self,
        *,
        data: dict,
        topic: Union[List, str],
        producer: KafkaProducer,
    ) -> None:
        """
        Сервис для отправки сгенерированного сообщения в брокер

        :param data: данные для отправки(словарь)
        :type data: `class: Dict[str, Any]`
        :param topic: топик куда данные будут отправлены
        :type topic: `class: Union[List, str]`
        """
        try:
            if isinstance(topic, str):
                logger.info(f"Data send to: '{topic}' topic")
                producer.send(topic=topic, value=data)
            elif isinstance(topic, list):
                logger.info(f"Data send to: {topic} topic")
                sequence_of_topics = topic
                for _topic in sequence_of_topics:
                    producer.send(topic=_topic, value=data)
            producer.flush()
        except Exception as e:
            logger.exception(f"Error occured when send message. Error is: {e}")
        finally:
            self._stop_producer()

    @logger.catch
    def _start_producer(self) -> KafkaProducer:
        """
        Создание продюсера

        :param boostrap_servers: адрес хоста для подключения к Kafka серверу
        :type boostrap_servers: str
        :return: обьект от AIOKafkaProducer
        :rtype: `class: aiokafka.AIOKafkaProducer`
        """
        try:
            producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_SERVER,
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                max_request_size=3718690
            )
            producer.start()
        except Exception as e:
            logger.exception(f"Error occured when created producer. Error is: {e}")
            return
        else:
            return producer

    @logger.catch
    def _stop_producer(self):
        self.producer.stop()
