"""Helper class for customer-related database operations."""

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.helpers.account_helper import AccountHelper
from app.helpers.transaction_helper import TransactionHelper
from app.interfaces.customer_interface import CustomerInterface
from app.models.customer import Customer


class CustomerHelper(CustomerInterface):
    """
    Helper class for customer-related database operations.
    """

    def __init__(self, db: Session):
        self.db: Session = db
        self.account_helper = AccountHelper(db)
        self.transaction_helper = TransactionHelper(db)

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
        try:
            return (
                self.db.query(Customer)
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
        try:
            self.db.add(customer)
            self.db.flush()
            self.db.refresh(customer)
            return customer

        except IntegrityError as e:
            raise e

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
