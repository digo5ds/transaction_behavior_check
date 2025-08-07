import os

from alembic import command
from alembic.config import Config

from app.core.postgres_database import DATABASE_URL


def run_migrations(database_url: str):
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    db_url = DATABASE_URL
    run_migrations(db_url)
