import os
from datetime import datetime, timedelta

from app.__version__ import get_version

# PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
POSTGRES_HOST = "localhost"

# MongoDB
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_DB = os.getenv("MONGO_DB")
MONGO_HOST = "localhost"


FASTAPI_CONFIG = {
    "title": "Transaction Behavior Check API",
    "description": "API to Simulate Financial Transaction Risk Calculation",
    "version": get_version(),
    "license_info": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    "openapi_tags": [
        {
            "name": "TransactionBehaviorCheck",
            "description": "API to Simulate Financial Transaction Risk Calculation",
        }
    ],
}


rules = {
    "alto_valor_atm_madrugada": [
        {
            "filter": {
                "$and": [
                    {
                        "field": "created_at",
                        "op": "$gte",
                        "value": datetime.now().replace(hour=0, minute=0, second=0),
                    },
                    {
                        "field": "created_at",
                        "op": "$lte",
                        "value": datetime.now().replace(hour=5, minute=0, second=0),
                    },
                    {
                        "field": "channel",
                        "op": "$eq",
                        "value": "ATM",
                    },
                    {
                        "field": "amount",
                        "op": "$gte",
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
                "$or": [
                    {
                        "$and": [
                            {
                                "field": "created_at",
                                "op": "$lt",
                                "value": datetime.now().replace(
                                    hour=10, minute=0, second=0
                                ),
                            },
                            {
                                "field": "channel",
                                "op": "$eq",
                                "value": "TELLER",
                            },
                        ]
                    },
                    {
                        "$and": [
                            {
                                "field": "created_at",
                                "op": "$gt",
                                "value": datetime.now().replace(
                                    hour=16, minute=0, second=0
                                ),
                            },
                            {
                                "field": "channel",
                                "op": "$eq",
                                "value": "TELLER",
                            },
                        ]
                    },
                ]
            },
            "suspect": True,
        },
    ],
    "multiples_txr_by_IBK_or_MBK": [
        {
            "filter": {
                "$and": [
                    {
                        "transform": "!count",
                        "params": {"channel": ["IBK", "MBK"]},
                        "op": "lte",
                        "value": 5,
                    },
                    {
                        "field": "created_at",
                        "op": "$gt",
                        "value": datetime.now() - timedelta(hours=1),
                    },
                ],
            },
            "suspect": True,
        }
    ],
    "same_trx_in_last_10_minutes": [
        {
            "filter": {
                "$and": [
                    {
                        "field": "created_at",
                        "op": "$gte",
                        "value": datetime.now() - timedelta(minutes=10),
                    },
                    {
                        "field": "transaction_id",  # ou algum identificador de transação
                        "transform": "!same_transaction",
                        "op": "$gte",
                        "value": 2,
                    },
                ]
            },
            "suspect": True,
        }
    ],
}
