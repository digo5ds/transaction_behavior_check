"""
This module provides a function to migrate the MongoDB database."""

from app.core.mongo_database import mongo_connection
from app.helpers.mongo_helper import MongoHelper
from app.models.collections.rules_model import Rule

INITIAL_RULES = {
    "high_value_dawn": [
        {
            "filter": {
                "and": [
                    {
                        "field": "created_at",
                        "transform": "!time",
                        "op": "gte",
                        "value": {"hour": 0, "minute": 0, "second": 0},
                    },
                    {
                        "field": "created_at",
                        "transform": "!time",
                        "op": "lte",
                        "value": {"hour": 5, "minute": 0, "second": 0},
                    },
                    {
                        "field": "channel",
                        "op": "eq",
                        "value": "ATM",
                    },
                    {
                        "field": "amount",
                        "op": "gte",
                        "value": 10000,
                    },
                ]
            },
            "suspect": True,
        }
    ],
    "trx_teller_bef_10__or_aft_16": [
        {
            "filter": {
                "or": [
                    {
                        "and": [
                            {
                                "field": "created_at",
                                "transform": "!time",
                                "op": "lt",
                                "value": {"hour": 10, "minute": 0, "second": 0},
                            },
                            {
                                "field": "channel",
                                "op": "eq",
                                "value": "TELLER",
                            },
                        ]
                    },
                    {
                        "and": [
                            {
                                "field": "created_at",
                                "transform": "!time",
                                "op": "gt",
                                "value": {"hour": 16, "minute": 0, "second": 0},
                            },
                            {
                                "field": "channel",
                                "op": "eq",
                                "value": "TELLER",
                            },
                        ]
                    },
                ]
            },
            "suspect": True,
        },
    ],
    "same_trx_in_last_in_period": [
        {
            "filter": {
                "and": [
                    {
                        "field": "",
                        "transform": "!count_same_trx_by_channel_user_in_last_in_period",
                        "params": {
                            "channel": ["IBK", "MBK", "TELLER", "ATM"],
                            "interval_minutes": 10,
                            "sensibility_variation_percentage": 0.2,
                        },
                        "op": "gte",
                        "value": 3,
                    }
                ]
            },
        },
    ],
    "high_value_account_destination_not_frequent": [
        {
            "filter": {
                "and": [
                    {
                        "field": "",
                        "transform": "!destination_account_frequency",
                        "op": "lte",
                        "value": 2,
                    },
                    {
                        "field": "amount",
                        "op": "gte",
                        "value": 10000,
                    },
                ]
            },
        },
    ],
    "high_value_older_age_diginal": [
        {
            "filter": {
                "and": [
                    {
                        "field": "origin_account_rel.customer_rel.age",
                        "op": "gte",
                        "value": 60,
                    },
                    {
                        "field": "amount",
                        "op": "gte",
                        "value": 500,
                    },
                    {
                        "field": "channel",
                        "op": "in",
                        "value": ["IBK", "MBK"],
                    },
                    {
                        "field": "",
                        "transform": "!count_same_trx_by_channel_user_in_last_in_period",
                        "params": {
                            "channel": ["IBK", "MBK"],
                            "interval_minutes": 43200,
                        },
                        "op": "lte",
                        "value": 5,
                    },
                ]
            },
        },
    ],
    "multiples_txr_by_IBK_or_MBK": [
        {
            "filter": {
                "$and": [
                    {
                        "transform": "!count_same_trx_by_channel_user_in_last_in_period",
                        "params": {"channel": ["IBK", "MBK"]},
                        "op": "lte",
                        "value": 5,
                    },
                    {
                        "field": "created_at",
                        "transform": "!time",
                        "op": "$gt",
                        "value": {"hour": 16, "minute": 0, "second": 0},
                    },
                ],
            },
            "suspect": True,
        }
    ],
}


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
