from events_gateway.models.abstract import IDBase, TimestampBase

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


class StatReceivedObjects(IDBase, TimestampBase):
    __tablename__ = "stat_received_objects"

    indicator_id = Column(UUID(as_uuid=True), nullable=True)
