"""MongoDB database factory."""

from contextlib import contextmanager

from mongoengine import connect, disconnect
from mongoengine.connection import get_db

from app.core.config import (
    MONGO_DB,
    MONGO_HOST,
    MONGO_PASSWORD,
    MONGO_PORT,
    MONGO_USERNAME,
)


@contextmanager
def mongo_connection():
    """
    Context manager for connecting to a MongoDB database.

    Establishes a connection to the MongoDB database using the provided
    configuration parameters and yields a database object. Ensures that
    the connection is properly closed when the context is exited.

    Yields:
        Database object: The MongoDB database object for performing
        operations within the context.
    """

    connect(
        db=MONGO_DB,
        host=MONGO_HOST,
        port=MONGO_PORT,
        username=MONGO_USERNAME,
        password=MONGO_PASSWORD,
    )
    try:
        yield get_db()
    finally:
        disconnect()
