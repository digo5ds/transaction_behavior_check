import os
from datetime import datetime, timedelta

from app.__version__ import get_version

# PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
POSTGRES_HOST = os.getenv("POSTGRES_CONTAINER_NAME")
# MongoDB
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_DB = os.getenv("MONGO_DB")
MONGO_HOST = os.getenv("MONGO_CONTAINER_NAME")

APPLICATION_PORT = int(os.getenv("APPLICATION_PORT"))

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
