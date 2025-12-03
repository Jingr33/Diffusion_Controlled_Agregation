import os

from alembic.config import Config
from alembic import command
from database.db_connect import ensure_database_exists

class DbRunner():
    """
    Manages database setup and migrations.
    """
    def __init__(self) -> None:
        """Initialize database and run all pending migrations."""
        ensure_database_exists()
        run_migrations()

def run_migrations() -> None:
    """Execute Alembic database migrations."""
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '../../alembic.ini'))
    command.upgrade(alembic_cfg, "head")