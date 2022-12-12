from config.log_conf import logger
from apps.models.base import SyncPostgresDriver

def create_migrations():
    with SyncPostgresDriver().session() as db:
        logger.info("Start executing migrations...")

        db.execute("create table if not exists pattern_storage ( id serial primary key, data text, created_at timestamp not null default CURRENT_TIMESTAMP)")
        db.execute("create table if not exists log_statistic ( id serial primary key, data  jsonb not null default '{}'::jsonb, created_at timestamp not null default CURRENT_TIMESTAMP)")

        db.flush()
        db.commit()
