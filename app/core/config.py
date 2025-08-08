import os

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
