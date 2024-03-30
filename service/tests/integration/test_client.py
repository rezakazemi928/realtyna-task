from unittest.mock import patch

from model import Client
from tests.test_base import BaseTestCase


class TestClientResource(BaseTestCase):
    @patch("model.Client.query")
    def test_get_clients(self, mock_query):
        mock_client1 = Client(id=1, username="Client 1")
        mock_client2 = Client(id=2, username="Client 2")
        mock_query.all.return_value = [mock_client1, mock_client2]
        response = self.app.get("/api/client")
        self.assertEqual(response.status_code, 200)

    @patch("model.Client.query")
    @patch("schema.ClientSchema")
    def test_create_new_client(self, mock_schema, mock_query):
        mock_request_data = {"username": "new_user"}
        mock_query.filter.return_value.first.return_value = None
        mock_schema_instance = mock_schema(partial=True)
        mock_schema_instance.load.return_value = Client(id=1, username="new_user")
        mock_schema.return_value = mock_schema_instance
        response = self.app.post("/api/client", json=mock_request_data)
        self.assertEqual(response.status_code, 200)

    @patch("model.Client.query")
    def test_existing_client(self, mock_query):
        mock_request_data = {"username": "existing_user"}
        mock_existing_client = Client(id=2, username="existing_user")
        mock_query.filter.return_value.first.return_value = mock_existing_client
        response = self.app.post("/api/client", json=mock_request_data)
        self.assertEqual(response.status_code, 409)
