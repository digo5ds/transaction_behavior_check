"""Helper class for customer-related database operations."""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.account import Account


class AccountHelper:

    def __init__(self, db: Session):
        self.db: Session = db

    def save_account(self, account: Account):
        try:
            self.db.add(account)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_account(self, account_data: Account):
        try:
            return (
                self.db.query(Account)
                .filter(
                    Account.agency == account_data.agency,
                    Account.account == account_data.account,
                )
                .first()
            )
        except SQLAlchemyError as e:
            raise e
