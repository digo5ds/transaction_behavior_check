from sqlalchemy import Column, Integer, String

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
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
