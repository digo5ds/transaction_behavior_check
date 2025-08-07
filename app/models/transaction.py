"""Models for representing transactions."""

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String

from app.core.constants import ChannelEnum
from app.core.postgres_database import Base


class Transaction(Base):
    """
    Represents a financial transaction between two accounts.

    Attributes:
        id (str): Unique identifier for the transaction.
        transaction_date (datetime): Date and time when the transaction occurred.
        amount (Decimal): Monetary value of the transaction.
        channel (ChanelEnum): Channel through which the transaction was made.
        origin_agency (str): Agency code of the account initiating the transaction.
        origin_account (str): Account number of the originator.
        destination_agency (str): Agency code of the destination account.
        destination_account (str): Account number of the recipient.
        suspect (int): Flag indicating if the transaction is considered suspicious.
    """

    __tablename__ = "transactions"

    id = Column(String(64), primary_key=True, index=True)
    transaction_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    channel = Column(Enum(ChannelEnum), nullable=False)
    origin_agency = Column(String, nullable=False)
    origin_account = Column(String, nullable=False)
    destination_agency = Column(String, nullable=False)
    destination_account = Column(String, nullable=False)
    suspect = Column(Integer, default=False)
