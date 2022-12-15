from events_gateway.config.log_conf import logger
from events_gateway.models.base import SyncPostgresDriver


def apply_migrations():
    with SyncPostgresDriver().session() as db:
        db.execute("CREATE TABLE IF NOT EXISTS stat_received_objects ( id SERIAL PRIMARY KEY,  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)") # noqa

        db.flush()
        db.commit()
        logger.info("Migrations applied...")
