from unittest.mock import patch

from model import Owner
from tests.test_base import BaseTestCase


class TestOwnerResource(BaseTestCase):
    @patch("model.Owner.query")
    @patch("schema.OwnerSchema")
    def test_create_new_client(self, mock_schema, mock_query):
        mock_request_data = {"username": "new_user"}
        mock_query.filter.return_value.first.return_value = None
        mock_schema_instance = mock_schema(partial=True)
        mock_schema_instance.load.return_value = Owner(id=1, username="new_user")
        mock_schema.return_value = mock_schema_instance
        response = self.app.post("/api/client", json=mock_request_data)
        self.assertEqual(response.status_code, 200)

    @patch("model.Owner.query")
    def test_existing_client(self, mock_query):
        mock_request_data = {"username": "existing_user"}
        mock_existing_owner = Owner(id=2, username="existing_user")
        mock_query.filter.return_value.first.return_value = mock_existing_owner
        response = self.app.post("/api/owner", json=mock_request_data)
        self.assertEqual(response.status_code, 409)
