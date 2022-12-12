import json

from apps.models.models import PatternStorage, LogStatistic
from apps.models.provider import PatternStorageProvider, LogStatisticProvider


def get_first_pattern() -> PatternStorage:
    return PatternStorageProvider().get_first()


def create_log_statistic(*, statistic: json) -> LogStatistic:
    return LogStatisticProvider().create(statistic=statistic)
