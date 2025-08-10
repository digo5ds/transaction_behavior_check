"""Helper class for account-related database operations."""

from sqlalchemy import case, cast, desc, func, literal, or_
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql.selectable import Subquery

from app.core.postgres_database import get_db
from app.interfaces.account_interface import AccountInterface
from app.models.tables.account_model import Account
from app.models.tables.customer_model import Customer
from app.models.tables.transaction_model import Transaction


class AccountHelper(AccountInterface):
    """
    Helper class for account-related database operations.
    """

    def save_account(self, account: Account):
        """
        Saves an account to the database.

        Args:
            account (Account): The account object to be saved.

        Raises:
            SQLAlchemyError: If an error occurs during the database operation,
                the transaction is rolled back and the exception is raised.
        """
        with get_db() as db:
            try:
                db.add(account)
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                raise e

    def __get_balance_subquery(self, account: Account, db: Session) -> Subquery:
        """
        Creates a subquery to calculate the balance of a given account.

        Args:
            account (Account): The account for which to calculate the balance.
            db (Session): The database session.

        Returns:
            Subquery: A SQLAlchemy subquery that calculates the balance by summing
                    the transaction amounts where the account is either the origin
                    or the destination. Credits are added and debits are subtracted.
        """

        balance_expr = func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.destination_account_id == account.id,
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ) - func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.origin_account_id == account.id,
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        )

        return (
            db.query(balance_expr.label("balance"))
            .filter(
                or_(
                    Transaction.origin_account_id == account.id,
                    Transaction.destination_account_id == account.id,
                )
            )
            .subquery()
        )

    def __get_transactions_subquery(
        self, account: Account, last_n: int, db: Session
    ) -> Subquery:
        """
        Constructs a subquery to retrieve a list of transactions for a given account.

        The query selects transaction details including transaction ID, creation date,
        transaction type (debit or credit), associated account and customer details, amount,
        and whether the transaction is marked as suspicious. It joins the transactions with
        the associated origin and destination accounts and their respective customers.

        Args:
            account (Account): The account for which transactions are to be retrieved.
            last_n (int, optional): The number of most recent transactions to retrieve.
                Defaults to 10.
            db (Session): The database session.

        Returns:
            Subquery: A SQLAlchemy subquery object representing the transaction details
            for the specified account, limited to the specified number of recent entries.
        """
        origin_acc = aliased(Account)
        dest_acc = aliased(Account)
        origin_cust = aliased(Customer)
        dest_cust = aliased(Customer)

        tx_query = (
            db.query(
                Transaction.id.label("tx_id"),
                Transaction.created_at,
                case(
                    (Transaction.origin_account_id == account.id, "debit"),
                    else_="credit",
                ).label("tx_type"),
                case(
                    (Transaction.origin_account_id == account.id, dest_acc.agency),
                    else_=origin_acc.agency,
                ).label("agencia"),
                case(
                    (Transaction.origin_account_id == account.id, dest_acc.account),
                    else_=origin_acc.account,
                ).label("conta"),
                case(
                    (Transaction.origin_account_id == account.id, dest_cust.name),
                    else_=origin_cust.name,
                ).label("nome"),
                case(
                    (Transaction.origin_account_id == account.id, dest_cust.age),
                    else_=origin_cust.age,
                ).label("idade"),
                Transaction.amount,
                Transaction.suspect,
            )
            .join(origin_acc, origin_acc.id == Transaction.origin_account_id)
            .join(origin_cust, origin_cust.id == origin_acc.customer_id)
            .join(dest_acc, dest_acc.id == Transaction.destination_account_id)
            .join(dest_cust, dest_cust.id == dest_acc.customer_id)
            .filter(
                or_(
                    Transaction.origin_account_id == account.id,
                    Transaction.destination_account_id == account.id,
                )
            )
            .order_by(desc(Transaction.created_at))
            .limit(last_n)
            .subquery()
        )

        # Retorna a query original (não executa), pois vamos usar json_agg na query principal
        return tx_query

    def get_account_report(self, account: Account, last_n=5) -> dict:
        """
        Retrieves an account report from the database.

        Args:
            account (Account): The account object whose report is to be retrieved.
            last_n (int): The number of last transactions to include in the report.

        Returns:
            AccountInfoResponse: The account report object.

        Raises:
            SQLAlchemyError: If an error occurs during the database operation,
                the exception is raised.
        """

        with get_db() as db:
            customer_subq = (
                db.query(Customer).filter(Customer.id == account.customer_id).subquery()
            )

            balance_subq = self.__get_balance_subquery(account, db)

            transactions_subq = self.__get_transactions_subquery(account, last_n, db)
            try:
                query = (
                    db.query(
                        customer_subq.c.name.label("nome"),
                        customer_subq.c.age.label("idade"),
                        balance_subq.c.balance,
                        func.coalesce(
                            func.json_agg(
                                func.json_build_object(
                                    "agencia",
                                    transactions_subq.c.agencia,
                                    "conta",
                                    transactions_subq.c.conta,
                                    "type",
                                    transactions_subq.c.tx_type,
                                    "valor",
                                    transactions_subq.c.amount,
                                    "nome",
                                    transactions_subq.c.nome,
                                    "idade",
                                    transactions_subq.c.idade,
                                    "suspect",
                                    transactions_subq.c.suspect,
                                )
                            ).filter(transactions_subq.c.tx_id.isnot(None)),
                            cast("[]", type_=JSON),
                        ).label("last_transactions"),
                    )
                    .select_from(customer_subq)
                    .join(balance_subq, literal(True))
                    .join(transactions_subq, literal(True))
                ).group_by(
                    customer_subq.c.name,
                    customer_subq.c.age,
                    balance_subq.c.balance,
                )

                result = query.first()

                if not result:
                    return None

                return {
                    "nome": result.nome,
                    "idade": result.idade,
                    "balance": float(result.balance),
                    "last_transactions": result.last_transactions or [],
                }
            except SQLAlchemyError as e:
                raise e

    def get_account(self, account_data: Account) -> Account | None:
        """
        Retrieves an account from the database.

        Args:
            account_data (Account): The agency and account numbers to be searched.

        Returns:
            Account: The account object if found, None otherwise.

        Raises:
            SQLAlchemyError: If an error occurs during the database operation,
                the transaction is rolled back and the exception is raised.
        """
        with get_db() as db:
            try:
                return (
                    db.query(Account)
                    .filter(
                        Account.agency == account_data.agency,
                        Account.account == account_data.account,
                    )
                    .first()
                )
            except SQLAlchemyError as e:
                raise e
