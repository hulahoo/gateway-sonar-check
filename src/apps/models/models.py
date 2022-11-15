from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import JSONB

from src.apps.models.abstract import TimestampBase, IDBase


class PatternStorage(IDBase, TimestampBase):

    __tablename__ = "pattern_storage"

    data = Column(Text())


class LogStatistic(IDBase, TimestampBase):

    __tablename__ = "log_statistic"

    data = Column(JSONB())
