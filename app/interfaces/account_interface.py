"""Interface for account_helper"""

from abc import ABC, abstractmethod

from app.models.tables.account_model import Account


class AccountInterface(ABC):
    """Interface for account_helper"""

    def insert(self, account: Account):
        """
        Saves an account to the database.

        Args:
            account (Account): The account object to be saved.

        Raises:
            NotImplementedError: If the method is not implemented in the concrete class.
        """
        raise NotImplementedError

    @abstractmethod
    def get_account_report(self, account: Account, last_n=5):
        """
        Retrieves an account report from the database.

        Args:
            account (Account): The account object whose report is to be retrieved.
            last_n (int): The number of last transactions to include in the report.

        Returns:
            AccountInfoResponse: The account report object.

        Raises:
            NotImplementedError: If the method is not implemented in the concrete class.
        """
        raise NotImplementedError
