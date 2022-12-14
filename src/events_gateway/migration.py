import alembic.config

from events_gateway.config.log_conf import logger


def execute_migrations():
    import os
    print(os.getcwd(), "?????????????")
    alembic_args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembic_args)
    logger.info("Migrations applied successfully")
