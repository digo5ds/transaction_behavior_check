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

    @patch("app.routes.customer_routes.CustomerHelper")
    def test_put_customer_success(self, mock_helper):
        # Mock comportamento do helper para simular criação OK
        mock_helper.return_value.save_customer_profile.return_value = None

        response = self.client.put("/api/customers/1/1", json=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"message": "Created"})

    def test_put_customer_bad_request_missing_key(self):
        response = self.client.put(
            "/api/customers/1/1", json=self.invalid_data_missing_key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_customer_bad_request_wrong_type(self):
        response = self.client.put(
            "/api/customers/1/1", json=self.invalid_data_wrong_type
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("app.routes.customer_routes.CustomerHelper")
    def test_put_customer_conflict(self, mock_helper):
        mock_helper.return_value.save_customer_profile.side_effect = IntegrityError(
            statement=None, params=None, orig=None
        )
        response = self.client.put("/api/customers/1/1", json=self.conflict_data)
        self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
