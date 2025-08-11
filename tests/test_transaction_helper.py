from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.helpers.transaction_helper import TransactionHelper
from app.models.tables.transaction_model import Transaction

simple_transaction = Transaction(
    id=1,
    amount=100,
    channel="online",
    origin_account_id=1,
    destination_account_id=2,
)


@pytest.fixture
def transaction_helper():
    return TransactionHelper()


@patch("app.helpers.transaction_helper.get_db")
def test_insert_success(mock_get_db, transaction_helper):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db

    # Mock refresh para não fazer nada
    mock_db.refresh.return_value = None

    result = transaction_helper.insert(simple_transaction)

    mock_db.add.assert_called_once_with(simple_transaction)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(simple_transaction)
    assert result == simple_transaction


@patch("app.helpers.transaction_helper.get_db")
def test_insert_raises_rollback(mock_get_db, transaction_helper):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db

    mock_db.commit.side_effect = SQLAlchemyError("fail commit")

    with pytest.raises(SQLAlchemyError):
        transaction_helper.insert(simple_transaction)

    mock_db.rollback.assert_called_once()


@patch("app.helpers.transaction_helper.get_db")
def test_count_transaction_by_user_channel_success(mock_get_db, transaction_helper):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db

    expected_result = [
        ("online", 50, 2, 1, 3),
        ("mobile", 30, 2, 1, 1),
    ]

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_join = mock_filter.join.return_value
    mock_group = mock_join.group_by.return_value
    mock_group.all.return_value = expected_result

    channel = ("online", "mobile")
    lookback = datetime.utcnow() - timedelta(days=1)
    origin_account_id = 1
    destination_account_id = 2

    result = transaction_helper.count_transaction_by_user_channel(
        channel, lookback, origin_account_id, destination_account_id
    )

    mock_db.query.assert_called_once()
    mock_filter.filter.assert_called()
    mock_join.join.assert_called_once()
    mock_group.group_by.assert_called_once()
    mock_group.all.assert_called_once()

    assert result == expected_result


@patch("app.helpers.transaction_helper.get_db")
def test_count_transaction_by_user_channel_raises_rollback(
    mock_get_db, transaction_helper
):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db

    mock_db.query.side_effect = SQLAlchemyError("query fail")

    with pytest.raises(SQLAlchemyError):
        transaction_helper.count_transaction_by_user_channel(
            ("online",), datetime.utcnow(), 1, 2
        )

    mock_db.rollback.assert_called_once()
