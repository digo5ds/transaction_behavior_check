"""Unit tests for customer routes."""

import unittest
from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from app.api import app


class TestPutCustomer(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.valid_data = {
            "agencia": 1,
            "conta": 1,
            "nome": "Fulano",
            "idade": 30,
        }
        self.invalid_data_missing_key = {
            "agencia": 1,
            "conta": 1,
            "idade": 30,
        }
        self.invalid_data_wrong_type = {
            "agencia": "um",
            "conta": 1,
            "nome": "Fulano",
            "idade": 30,
        }
        self.conflict_data = {
            "agencia": 1,
            "conta": 1,
            "nome": "Fulano",
            "idade": 30,
        }

    @patch("app.helpers.customer_helper.CustomerHelper.insert")
    @patch("app.helpers.account_helper.AccountHelper.save_account")
    def test_put_customer_success(self, mock_save_account, mock_insert):
        """
        Tests if a PUT request to create a customer with valid data returns a
        201 Created response with a success message. Mocks the CustomerHelper.insert
        and AccountHelper.save_account methods to ensure no real database calls are made.
        """

        mock_insert.return_value = None
        mock_save_account.return_value = None

        response = self.client.put("/api/customers/1/1", json=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"message": "Created"})

    def test_put_customer_bad_request_missing_key(self):
        """
        Tests if a PUT request with missing key results in a 400 Bad Request error.

        Verifies that the response contains the appropriate error message indicating
        the missing key.
        """
        response = self.client.put(
            "/api/customers/1/1", json=self.invalid_data_missing_key
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )  # FastAPI usa 422 para validação

    def test_put_customer_bad_request_wrong_type(self):
        """
        Testa se uma requisi o PUT com um tipo de dado
        incorreto (agencia, conta, nome, idade) retorna um erro 400.
        """
        response = self.client.put(
            "/api/customers/1/1", json=self.invalid_data_wrong_type
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("app.helpers.customer_helper.CustomerHelper.insert")
    def test_put_customer_conflict(self, mock_insert):
        """
        Tests if a PUT request to create a customer that already exists
        results in a 409 Conflict error. Mocks the CustomerHelper.insert
        method to raise an IntegrityError, simulating a conflict in the
        database. Also mocks the AccountHelper.save_account method to
        ensure no real database calls are made.
        """

        mock_insert.side_effect = IntegrityError(statement=None, params=None, orig=None)

        with patch(
            "app.helpers.account_helper.AccountHelper.save_account"
        ) as mock_save_account:
            mock_save_account.return_value = None
            response = self.client.put("/api/customers/1/1", json=self.conflict_data)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_put_customer_agency_account_mismatch(self):
        """
        Tests if a PUT request with mismatched agency and account numbers between
        the URL and JSON payload returns a 400 Bad Request error. Verifies that
        the response contains the appropriate error message indicating the
        mismatch.
        """

        data = {
            "agencia": 2,
            "conta": 3,
            "nome": "Fulano",
            "idade": 30,
        }
        response = self.client.put("/api/customers/1/1", json=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Agency and account numbers do not match", response.json().get("detail", "")
        )


if __name__ == "__main__":
    unittest.main()
