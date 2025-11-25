import os

from alembic.config import Config
from alembic import command
from database.db_connect import ensure_database_exists

class DbRunner():
    def __init__(self) -> None:
        ensure_database_exists()
        run_migrations()

def run_migrations():
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '../../alembic.ini'))
    command.upgrade(alembic_cfg, "head")