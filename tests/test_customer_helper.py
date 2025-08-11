# tests/test_customer_helper.py
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.helpers.customer_helper import CustomerHelper
from app.models.tables.customer_model import Customer

simple_customer = Customer(id=1, name="José Almeida")  # variável global simples


@pytest.fixture
def helper():
    return CustomerHelper()


def test_get_customer_by_id_success(helper):
    mock_session = MagicMock()
    mock_session.query().filter().first.return_value = simple_customer
    mock_customer_input = MagicMock(customer_id=1)  # simula o objeto de entrada

    with patch(
        "app.helpers.customer_helper.get_db",
        return_value=MagicMock(
            __enter__=lambda s: mock_session,
            __exit__=lambda s, a, b, c: None,
        ),
    ):
        result = helper.get_customer_by_id(mock_customer_input)

    assert result == simple_customer
    mock_session.query().filter().first.assert_called_once()


def test_get_customer_by_id_sqlalchemy_error(helper):
    mock_session = MagicMock()
    mock_session.query().filter().first.side_effect = SQLAlchemyError("DB error")
    mock_customer_input = MagicMock(customer_id=1)

    with patch(
        "app.helpers.customer_helper.get_db",
        return_value=MagicMock(
            __enter__=lambda s: mock_session,
            __exit__=lambda s, a, b, c: None,
        ),
    ):
        with pytest.raises(SQLAlchemyError):
            helper.get_customer_by_id(mock_customer_input)


def test_insert_success(helper):
    mock_session = MagicMock()

    with patch(
        "app.helpers.customer_helper.get_db",
        return_value=MagicMock(
            __enter__=lambda s: mock_session,
            __exit__=lambda s, a, b, c: None,
        ),
    ):
        result = helper.insert(simple_customer)

    mock_session.add.assert_called_once_with(simple_customer)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(simple_customer)
    assert result == simple_customer


def test_insert_integrity_error(helper):
    mock_session = MagicMock()
    mock_session.add.side_effect = IntegrityError("stmt", "params", "orig")

    with patch(
        "app.helpers.customer_helper.get_db",
        return_value=MagicMock(
            __enter__=lambda s: mock_session,
            __exit__=lambda s, a, b, c: None,
        ),
    ):
        with pytest.raises(IntegrityError):
            helper.insert(simple_customer)


def test_insert_sqlalchemy_error(helper):
    mock_session = MagicMock()
    mock_session.add.side_effect = SQLAlchemyError("DB error")

    with patch(
        "app.helpers.customer_helper.get_db",
        return_value=MagicMock(
            __enter__=lambda s: mock_session,
            __exit__=lambda s, a, b, c: None,
        ),
    ):
        with pytest.raises(SQLAlchemyError):
            helper.insert(simple_customer)

    mock_session.rollback.assert_called_once()


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__]))
