"""Helper class for customer-related database operations."""

from sqlalchemy import case, desc, func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.helpers.account_helper import AccountHelper
from app.interfaces.customer_interfaces import CustomerInterface
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import PutTransactionRequest


class TransactionHelper:
    """
    Helper class for customer-related database operations.

    This class implements methods to interact with the customer data in the database,
    such as saving customer profiles.

    Attributes:
        db (Session): SQLAlchemy database session used for database operations.

    Methods:
        save_custoxmer_profile(customer_data: PutCustomerRequest):
    """

    def __init__(self, db: Session):
        self.db: Session = db
        self.account_helper = AccountHelper(db)

    def save_transaction(self, transactionr_data: PutTransactionRequest):
        """
        Saves a customer profile into the database.

        Args:
            customer_data (PutCustomerRequest): The customer data to be saved.

        Returns:
            Customer: The saved customer object.
        """
        try:
            transaction = Transaction()
            transaction.id = transactionr_data.id_da_transacao
            transaction.created_at = transactionr_data.data_de_criacao
            transaction.origin_account_id = transactionr_data.id_da_conta_de_origem
            transaction.dest_account_id = transactionr_data.id_da_conta_de_destino
            transaction.amount = transactionr_data.valor_da_transacao
            transaction.channel = transactionr_data.canal
            transaction.type = transactionr_data.tipo
            transaction.suspect = False  # calcula risco

            self.db.add(transaction)
            self.db.commit()

        except SQLAlchemyError as e:
            # TODO: implements logger
            self.db.rollback()
            raise e

    def get_balance_by_account(self, account_data: Account) -> float:
        try:
            balance = (
                self.db.query(
                    func.sum(
                        case(
                            [
                                (
                                    Transaction.origin_account_id == account_data.id,
                                    -Transaction.amount,
                                ),
                                (
                                    Transaction.dest_account_id == account_data.id,
                                    Transaction.amount,
                                ),
                            ],
                            else_=0,
                        )
                    )
                )
                .filter(
                    or_(
                        Transaction.origin_account_id == account_data.id,
                        Transaction.dest_account_id == account_data.id,
                    )
                )
                .scalar()
            )
        except SQLAlchemyError as e:
            # TODO: implements logger
            raise e

        return balance

    def get_last_transactions_by_account(
        self, account: Account, limit: int
    ) -> list[Transaction]:
        try:
            return (
                self.db.query(Transaction)
                .filter(
                    or_(
                        Transaction.origin_account_id == account.id,
                        Transaction.dest_account_id == account.id,
                    )
                )
                .order_by(desc(Transaction.created_at))
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            # TODO: implements logger
            raise e
