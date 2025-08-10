"""Interface for financial transaction entities"""

from abc import ABC, abstractmethod

from app.models.tables.transaction_model import Transaction


class TransactionInterface(ABC):
    """
    Abstract base class that defines the interface for a transaction object.
    """

    @abstractmethod
    def insert(self, transaction: Transaction):
        """
        Save a transaction record into the database.

        Args:
            transaction (Transaction): The transaction data to be saved.

        Raises:
            NotImplementedError: This method must be overridden in a subclass.
        """
        raise NotImplementedError
