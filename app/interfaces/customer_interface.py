"""Interface for customer_helper"""

from abc import ABC, abstractmethod

from app.models.customer_model import Customer


class CustomerInterface(ABC):
    """
    Abstract base class that defines the interface for a customer object.
    """

    @abstractmethod
    def insert(self, customer: Customer):
        """
        Saves a customer profile into the database.

        Args:
            customer_data (PutCustomerRequest): The customer data to be saved.

        Returns:
            Customer: The saved customer object.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_customer_by_id(self, customer: Customer):
        """
        Retrieves a customer by their customer ID.

        Args:
            customer (Customer): The customer object containing the ID to be retrieved.

        Returns:
            Customer: The retrieved customer object.

        Raises:
            SQLAlchemyError: If an error occurs during the database query.
        """
        raise NotImplementedError()
