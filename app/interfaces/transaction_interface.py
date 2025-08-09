"""Interface for financial transaction entities"""

from abc import ABC, abstractmethod

from app.models.transaction import Transaction


class TransactionInterface(ABC):
    """
    Abstract base class that defines the interface for a transaction object.
    """

    @abstractmethod
    def insert(self, transaction: Transaction):
        pass
