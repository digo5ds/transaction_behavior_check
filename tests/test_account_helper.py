from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.helpers.account_helper import AccountHelper
from app.models.tables.account_model import Account

sample_account = Account(id=1, agency="123", account="456", customer_id=10)


@pytest.fixture
def account_helper():
    return AccountHelper()


@patch("app.helpers.account_helper.get_db")
def test_save_account_success(mock_get_db, account_helper):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db

    account_helper.save_account(sample_account)

    mock_db.add.assert_called_once_with(sample_account)
    mock_db.commit.assert_called_once()
    mock_db.rollback.assert_not_called()


@patch("app.helpers.account_helper.get_db")
def test_save_account_failure(mock_get_db, account_helper):
    mock_db = MagicMock()
    mock_db.commit.side_effect = SQLAlchemyError("fail")
    mock_get_db.return_value.__enter__.return_value = mock_db

    with pytest.raises(SQLAlchemyError):
        account_helper.save_account(sample_account)

    mock_db.add.assert_called_once_with(sample_account)
    mock_db.commit.assert_called_once()
    mock_db.rollback.assert_called_once()


@patch("app.helpers.account_helper.get_db")
def test_get_account_success(mock_get_db, account_helper):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = sample_account
    mock_get_db.return_value.__enter__.return_value = mock_db

    result = account_helper.get_account(sample_account)
    assert result == sample_account


@patch("app.helpers.account_helper.get_db")
def test_get_account_failure(mock_get_db, account_helper):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.side_effect = SQLAlchemyError(
        "fail"
    )
    mock_get_db.return_value.__enter__.return_value = mock_db

    with pytest.raises(SQLAlchemyError):
        account_helper.get_account(sample_account)


if __name__ == "__main__":
    pytest.main([__file__])
