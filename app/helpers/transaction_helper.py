"""Helper class for customer-related database operations."""

from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from app.core.logger import logger
from app.core.postgres_database import get_db
from app.interfaces.transaction_interface import TransactionInterface
from app.models.tables.transaction_model import Transaction


class TransactionHelper(TransactionInterface):
    """
    Helper class for customer-related database operations
    """

    def insert(self, transaction: Transaction) -> Transaction:
        """
        Saves a customer profile into the database.

        Args:
            customer_data (PutCustomerRequest): The customer data to be saved.

        Returns:
            Customer: The saved customer object.
        """
        with get_db() as db:
            try:
                db.add(transaction)
                db.commit()
                db.refresh(transaction)
                return transaction
            except SQLAlchemyError as e:
                db.rollback()
                raise e

    def count_transaction_by_user_channel(
        self,
        channel: tuple,
        lookback: datetime,
        origin_account_id: int,
        destination_account_id: int,
    ) -> list:
        """
        Counts how many transactions a given user has done in the last lookback time period
        in the given channels.

        Args:
            channel (tuple): The list of channels to filter the query.
            lookback (datetime): Timestamp from which to start counting transactions.
            origin_account_id (int): The user that did the transactions.

        Returns:
            list: A list of tuples with the channel, amount, destination_account_id and count of transactions.
        """
        with get_db() as db:
            try:
                return (
                    db.query(
                        Transaction.channel,
                        Transaction.amount,
                        Transaction.destination_account_id,  # incluído aqui
                        Transaction.origin_account_id,
                        # pylint: disable=not-callable
                        func.count(Transaction.id).label("count"),
                    )
                    .filter(
                        Transaction.channel.in_(channel),
                        Transaction.created_at > lookback,
                        Transaction.origin_account_id == origin_account_id,
                        Transaction.destination_account_id == destination_account_id,
                    )
                    .join(Transaction.destination_account_rel)
                    .group_by(
                        Transaction.channel,
                        Transaction.amount,
                        Transaction.destination_account_id,
                        Transaction.origin_account_id,  # incluído aqui também
                    )
                    .all()
                )
            except SQLAlchemyError as e:
                logger.error("Error counting transactions", exc_info=True)
                db.rollback()
                raise e
