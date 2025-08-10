"""
This module provides a function to migrate the MongoDB database."""

import alembic
from app.core.constants import INITIAL_RULES
from app.core.mongo_database import mongo_connection
from app.helpers.mongo_helper import MongoHelper
from app.models.collections.requests_model import RequestLog
from app.models.collections.rules_model import Rule
from app.models.collections.user_cache_model import KnowlegedDestinations


def migrate_mongo():
    """
    Ensures the indexes for the RequestLog and KnowlegedDestinations collections exist.

    This function is intended to be used as a one-time operation to create the indexes
    for the MongoDB collections. It should be called from the command-line interface.
    """
    with mongo_connection():
        # RequestLog.ensure_indexes()
        KnowlegedDestinations.ensure_indexes()
        RequestLog.ensure_indexes()
        Rule.ensure_indexes


def migrate_postgres():
    """
    Runs the Alembic migrations for the PostgreSQL database.

    This function is intended to be used as a one-time operation to apply the
    database migrations. It should be called from the command-line interface.
    """
    alembic.command.upgrade("alembic.ini", "head")


def populate_rules():
    """
    Populates the rules collection with the initial rules.

    This function is intended to be used as a one-time operation to populate the
    rules collection with the initial rules. It should be called from the
    command-line interface.

    """
    with mongo_connection():
        mongo_helper = MongoHelper()
        for name, conditions in INITIAL_RULES.items():
            mongo_helper.save(Rule(name=name, conditions=conditions))

    # migrate_postgres()


if __name__ == "__main__":
    try:
        migrate_mongo()
        populate_rules()
        migrate_postgres()
    except Exception as e:
        print(e)
