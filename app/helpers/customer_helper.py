"""Helper class for customer-related database operations."""

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.postgres_database import get_db
from app.helpers.account_helper import AccountHelper
from app.helpers.transaction_helper import TransactionHelper
from app.interfaces.customer_interface import CustomerInterface
from app.models.tables.customer_model import Customer


class CustomerHelper(CustomerInterface):
    """
    Helper class for customer-related database operations.
    """

    def __init__(self):
        self.account_helper = AccountHelper()
        self.transaction_helper = TransactionHelper()

    def get_customer_by_id(self, customer: Customer) -> Customer:
        """
        Retrieves a customer by their account.

        Args:
            customer (Customer): The customer to be retrieved.

        Returns:
            Customer: The retrieved customer object.

        Raises:
            SQLAlchemyError: If an error occurs during the database query.
        """
        with get_db() as db:
            try:
                return (
                    db.query(Customer)
                    .filter(Customer.id == customer.customer_id)
                    .first()
                )
            except SQLAlchemyError as e:
                raise e

    def insert(self, customer: Customer) -> Customer:
        """
        Saves a customer profile into the database.

        Args:
            customer_data (PutCustomerRequest): The customer data to be saved.

        Returns:
            Customer: The saved customer object.
        """
        with get_db() as db:
            try:
                db.add(customer)
                db.commit()
                db.refresh(customer)
                return customer

            except IntegrityError as e:
                raise e

            except SQLAlchemyError as e:
                db.rollback()
                raise e

    def delete(self, customer: Customer):
        try:
            with get_db() as db:
                db.delete(customer)
                db.commit()
        except SQLAlchemyError as e:
            raise e
