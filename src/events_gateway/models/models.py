from events_gateway.models.abstract import IDBase, TimestampBase


class StatReceivedObjects(IDBase, TimestampBase):
    __tablename__ = "stat_received_objects"
