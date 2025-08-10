from typing import List, Optional, Type

from mongoengine import Document
from pymongo.errors import PyMongoError

from app.core.mongo_database import mongo_connection
from app.interfaces.mongo_helper_interface import MongoHelperInterface


class MongoHelper(MongoHelperInterface):
    """
    Helper class for MongoDB operations.
    """

    def save(self, document: Document):
        """
        Saves a document into the MongoDB collection.

        Args:
            document (Document): A MongoEngine document to be saved.

        Raises:
            PyMongoError: If an error occurs during the insertion.
        """
        with mongo_connection():
            try:
                document.save()
            except PyMongoError as e:
                raise e

    def find_documents(
        self, document: Type[Document], filters: Optional[dict] = None, limit: int = 0
    ) -> List[Document]:
        """
        Searches for documents in the specified MongoDB collection.

        Args:
            document (Type[Document]): The model class to query, representing a MongoDB collection.
            filters (Optional[dict]): A dictionary containing the query filters to apply.
            limit (int): The maximum number of documents to return. A value of 0 means no limit.

        Returns:
            List[Document]: A list of documents matching the query criteria.

        Raises:
            PyMongoError: If an error occurs during the query operation.
        """

        with mongo_connection():
            try:

                query = document.objects

                if filters:
                    query = query.filter(**filters)

                if limit > 0:
                    query = query.limit(limit)

                return list(query)
            except PyMongoError as e:
                raise e
