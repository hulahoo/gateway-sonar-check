import json

from src.apps.models.provider import PatternStorageProvider, LogStatisticProvider
from src.apps.models.models import PatternStorage, LogStatistic


def get_first_pattern() -> PatternStorage:
    return PatternStorageProvider().get_first()


def create_log_statistic(*, statistic: json) -> LogStatistic:
    return LogStatisticProvider().create(statistic=statistic)
