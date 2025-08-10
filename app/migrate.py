"""
This module provides a function to migrate the MongoDB database."""

from app.core.constants import INITIAL_RULES
from app.core.mongo_database import mongo_connection
from app.helpers.mongo_helper import MongoHelper
from app.models.collections.rules_model import Rule


def populate_rules():
    """
    Populates the rules collection with the initial rules.

    This function is intended to be used as a one-time operation to populate the
    rules collection with the initial rules. It should be called from the
    command-line interface.

    """
    try:
        with mongo_connection():
            mongo_helper = MongoHelper()
            for name, conditions in INITIAL_RULES.items():
                mongo_helper.save(Rule(name=name, conditions=conditions))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    populate_rules()
