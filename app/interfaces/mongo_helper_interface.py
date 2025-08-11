"""interface for mongo_helper"""

from abc import ABC, abstractmethod
from typing import List, Optional, Type

from mongoengine import Document


class MongoHelperInterface(ABC):
    """
    Interface abstrata para operações MongoDB usando MongoEngine.
    """

    @abstractmethod
    def save(self, document: Document) -> Document:
        """
        Inserts a document into the collection.

        Args:
            document (Type[Document]): MongoEngine document class.
            data (dict): The data to be inserted.

        Returns:
            Document: The inserted document.

        Raises:
            Exception: If any error occurs during the insertion.
        """
        raise NotImplementedError

    @abstractmethod
    def find_documents(
        self,
        document: Type[Document],
        filters: Optional[dict] = None,
        limit: int = 0,
    ) -> List[Document]:
        """
        Searches documents in the collection associated with the MongoEngine model.

        Args:
            document (Type[Document]): The model class (e.g., User, RequestLog, etc.).
            filters (Optional[dict]): Dictionary with query filters (e.g., {"name": "Diogo"}).
            limit (int): Maximum number of documents to return (0 = no limit).

        Returns:
            List[Document]: List of found documents (instances of the model).
        """

        raise NotImplementedError
