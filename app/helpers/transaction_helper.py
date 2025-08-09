"""Helper class for customer-related database operations."""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.helpers.account_helper import AccountHelper
from app.interfaces.transaction_interface import TransactionInterface
from app.models.transaction import Transaction


class TransactionHelper(TransactionInterface):
    """
    Helper class for customer-related database operations
    """

    def __init__(self, db: Session):
        self.db: Session = db
        self.account_helper = AccountHelper(db)

    def insert(self, transaction: Transaction) -> Transaction:
        """
        Saves a customer profile into the database.

        Args:
            customer_data (PutCustomerRequest): The customer data to be saved.

        Returns:
            Customer: The saved customer object.
        """
        try:
            self.db.add(transaction)
            self.db.commit()

            return transaction
        except SQLAlchemyError as e:
            # TODO: implements logger
            self.db.rollback()
            raise e
