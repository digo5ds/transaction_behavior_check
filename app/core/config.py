import os
from datetime import datetime, timedelta

from app.__version__ import get_version

# PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTIGRES_HOST = "localhost"

# MongoDB
MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_PORT = os.getenv("MONGO_PORT")
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
                        "value": 1000,
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
                        "field": "transaction_id",
                        "transform": "!count",
                        "params": {"channel": ["IBK", "MBK"]},
                        "op": "$gte",
                        "value": 2,
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
