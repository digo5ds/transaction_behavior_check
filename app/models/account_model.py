from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.postgres_database import Base


class Account(Base):
    """
    Represents a bank account entity.

    Attributes:
        id (int): Primary key, unique identifier for the account.
        account (int): Account number.
        agency (int): Agency (branch) number.
        customer (Customer): Relationship to the Customer entity.
        customer_id (int): Foreign key referencing the associated customer.

    Constraints:
        UniqueConstraint on ('agency', 'account') to ensure each account number is unique within an agency.
    """

    __tablename__ = "account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(Integer)
    agency = Column(Integer)
    rel_customer = relationship("Customer")
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    __table_args__ = (UniqueConstraint("agency", "account", name="uq_agency_account"),)
