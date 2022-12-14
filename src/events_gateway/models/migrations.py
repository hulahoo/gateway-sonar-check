import os
import alembic.config

def execute_migrations():
    os.chdir("src/")
    alembicArgs = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembicArgs)
