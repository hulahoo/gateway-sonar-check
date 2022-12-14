from events_gateway.models.base import SyncPostgresDriver
from events_gateway.models.models import StatReceivedObjects


class StatReceivedProvider:
    def create(self) -> StatReceivedObjects:
        with SyncPostgresDriver().session() as db:
            received_object = StatReceivedObjects()

            db.add(received_object)
            db.flush()
            db.commit()


stat_received_provider = StatReceivedProvider()
