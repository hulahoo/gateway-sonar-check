import os
import alembic.config

def execute_migrations():
    os.chdir("src/")
    alembic_args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembic_args)
