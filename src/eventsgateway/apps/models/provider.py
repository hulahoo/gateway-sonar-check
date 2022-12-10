import json

from sqlalchemy import select, desc

from src.eventsgateway.apps.models.base import SyncPostgresDriver
from src.eventsgateway.apps.models.models import PatternStorage, LogStatistic


class PatternStorageProvider:
    """
    Интерфейс для предоставления запрос в таблицу PatternStorage
    """
    def get_first(self) -> PatternStorage:
        with SyncPostgresDriver().session() as db:
            query = select(PatternStorage).order_by(desc(PatternStorage.id))
            pattern_storage = db.execute(query)
            return pattern_storage.scalars().first()


class LogStatisticProvider:
    """
    Интерфейс для предоставления запрос в таблицу LogStatistic
    """
    def create(self, statistic: json) -> LogStatistic:
        with SyncPostgresDriver().session() as db:
            log_statistic = LogStatistic(data=statistic)

            db.add(log_statistic)
            db.flush()
            db.commit()
            db.refresh(log_statistic)
            return log_statistic
