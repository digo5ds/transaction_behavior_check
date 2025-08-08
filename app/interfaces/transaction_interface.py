"""Interface for financial transaction entities"""

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from app.core.constants import ChannelEnum


class TransactionInterface(ABC):
    """
    Abstract base class that defines the interface for a transaction object.

    Attributes:
        transaction_id (str): Unique identifier for the transaction.
        timestamp (datetime): Date and time when the transaction occurred.
        amount (Decimal): Monetary value of the transaction.
        channel (ChannelEnum): Channel through which the transaction was made.
        origin_agency (int): Identifier of the originating agency for the transaction.
    """

    @property
    @abstractmethod
    def transaction_id(self) -> str:
        pass

    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        pass

    @property
    @abstractmethod
    def amount(self) -> Decimal:
        pass

    @property
    @abstractmethod
    def channel(self) -> ChannelEnum:
        pass

    @property
    @abstractmethod
    def origin_agency(self) -> int:
        pass
