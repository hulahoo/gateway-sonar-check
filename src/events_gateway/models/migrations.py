import os
import alembic.config

from events_gateway.config.log_conf import logger

def execute_migrations():
    os.chdir("src/")
    alembic_args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembic_args)
    logger.info("Migrations applied successfully")
