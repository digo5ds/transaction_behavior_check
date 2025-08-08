"""Helper class for customer-related database operations."""

from sqlalchemy import desc, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.helpers.account_helper import AccountHelper
from app.helpers.transaction_helper import TransactionHelper
from app.interfaces.customer_interfaces import CustomerInterface
from app.models.account import Account
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.schemas.customer import (
    GetCustomerRequest,
    GetCustomerResponse,
    PutCustomerRequest,
)


class CustomerHelper(CustomerInterface):
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
        self.transaction_helper = TransactionHelper(db)

    def get_customer_by_account(self, costomer: Customer) -> Customer:
        try:
            return (
                self.db.query(Customer)
                .filter(Customer.id == costomer.customer_id)
                .first()
            )
        except SQLAlchemyError as e:
            raise e

    def save_customer_profile(self, customer: Customer, account: Account):
        """
        Saves a customer profile into the database.

        Args:
            customer_data (PutCustomerRequest): The customer data to be saved.

        Returns:
            Customer: The saved customer object.
        """
        try:
            # Inicia a transação
            self.db.add(customer)
            self.db.flush()  # para gerar o ID do customer antes de usar

            account.customer_id = customer.id
            self.account_helper.save_account(account)  # precisa usar mesma sessão

            self.db.commit()  # confirma tudo de uma vez
            self.db.refresh(customer)

            return customer

        except IntegrityError as e:
            raise e

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_customer_info(self, customer_data: GetCustomerRequest) -> Customer:
        """
        Retrieves customer information, including account details, recent transactions, and balance.

        Args:
            customer_data (GetCustomerRequest): An object containing the agency and account information to identify the customer.

        Returns:
            GetCustomerResponse: An object containing the customer's name, age, last 5 transactions (as either origin or destination), and current balance.
            Returns None if the account is not found.

        Notes:
            - The balance is calculated as the sum of credits (incoming transactions) minus debits (outgoing transactions) for the account.
            - The last 5 transactions are ordered by timestamp in descending order.
        """
        # Gets the customer's account (assuming agency + account)
        account = self.account_helper.get_account(
            Account(customer_data.agencia, customer_data.conta)
        )

        # Fetch the last 5 transactions where the account is either origin or destination
        last_transactions = self.transaction_helper.get_last_transactions_by_account(
            account=account,
            limit=5,
        )

        balance = self.transaction_helper.get_balance_by_account(account)

        # Gets the customer data
        customer = self.get_customer_by_account(account)

        customer_response = GetCustomerResponse(
            nome=customer.name,
            idade=customer.age,
            last_transactions=last_transactions,
            balance=balance,
        )

        return customer_response
