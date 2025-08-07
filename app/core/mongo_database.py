"""MongoDB database factory."""

from pymongo import MongoClient

MONGO_URI = "mongodb://mongo_user:mongo_pass@mongo:27017"
client = MongoClient(MONGO_URI)


def get_transaction_database():
    """
    Retrieves the 'transactions_db' database from the MongoDB client.

    Returns:
        Database: The MongoDB database instance for 'transactions_db'.
    """

    return client["transactions_db"]
