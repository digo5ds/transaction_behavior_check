"""Models for representing customers."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
)
from sqlalchemy.orm import relationship

from app.core.postgres_database import Base


class Transaction(Base):
    """
    Represents a financial transaction between two accounts.

    Attributes:
        id (int): Primary key, unique identifier for the transaction.
        created_at (datetime): Timestamp when the transaction record was created.
        amount (Decimal): The monetary value of the transaction.
        channel (ChannelEnum): The channel through which the transaction was made.
        suspect (bool): Indicates if the transaction is flagged as suspicious.
        type (TransactionType): The type/category of the transaction.
        origin_account_id (int): Foreign key referencing the originating account.
        destination_account_id (int): Foreign key referencing the destination account.
        origin_account_rel (Account): Relationship to the originating Account object.
        destination_account_rel (Account): Relationship to the destination Account object.

    Constraints:
        - The 'amount' field must be greater than 0.
    """

    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    channel = Column(Integer, nullable=False)
    suspect = Column(Boolean, default=False)
    # Foreign keys
    origin_account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    destination_account_id = Column(Integer, ForeignKey("account.id"), nullable=False)

    # Relationship
    origin_account_rel = relationship("Account", foreign_keys=[origin_account_id])

    destination_account_rel = relationship(
        "Account", foreign_keys=[destination_account_id]
    )

    # Constraint
    __table_args__ = (CheckConstraint("amount > 0", name="check_amount_positive"),)
