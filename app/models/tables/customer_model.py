from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.postgres_database import Base


class Customer(Base):
    """
    Represents a customer in the system.

    Attributes:
        id (int): Primary key, unique identifier for the customer.
        name (str): Name of the customer. Cannot be null.
        age (int): Age of the customer. Cannot be null.
    """

    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    accounts = relationship(
        "Account", back_populates="customer_rel", cascade="all, delete-orphan"
    )
