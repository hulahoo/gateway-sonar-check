from sqlalchemy import inspect
from sqlalchemy.engine.base import Engine

from events_gateway.config.log_conf import logger
from events_gateway.models.base import SyncPostgresDriver
from events_gateway.models.models import StatReceivedObjects


def apply_migrations() -> None:
    """Create migrations for Database"""
    engine: Engine = SyncPostgresDriver()._engine
    tables_list = [StatReceivedObjects.__tablename__]

    if not inspect(engine).has_table("stat_checked_objects"):
        StatReceivedObjects.__table__.create(engine)
        tables_list.remove(StatReceivedObjects.__tablename__)
        logger.info("Table StatReceivedObjects created")

    logger.info(f"Tables already exists: {tables_list}")
    logger.info("Migration applied successfully")
