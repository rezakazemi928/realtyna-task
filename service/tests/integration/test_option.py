from datetime import datetime
from unittest.mock import patch

from model import Client, ClientReservationList, Owner, ReserveOption
from tests.test_base import BaseTestCase


class TestReservationOptionResource(BaseTestCase):
    @patch("schema.ReserveOptionSchema")
    @patch("model.Owner.query")
    def test_create_reservation_option(self, mock_query, mock_schema):
        mock_request_data = {
            "option_type": "Option A",
            "owner": {"id": 1, "username": "user123"},
        }
        mock_owner = Owner(id=1, username="user123")
        mock_query.filter.return_value.first.return_value = mock_owner
        mock_schema_instance = mock_schema(partial=True)
        mock_schema_instance.load.return_value = ReserveOption(
            id=1, option_type="Option A", owner=mock_owner
        )
        mock_schema.return_value = mock_schema_instance
        response = self.app.post("/api/owner/options", json=mock_request_data)
        self.assertEqual(response.status_code, 200)

    @patch("model.Owner.query")
    def test_owner_not_found(self, mock_query):
        mock_request_data = {
            "option_type": "Option B",
            "owner": {"id": 2, "username": "nonexistent_user"},
        }
        mock_query.filter.return_value.first.return_value = None
        response = self.app.post("/api/owner/options", json=mock_request_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("owner cannot be found", response.json["msg"]["_schema"])

    @patch("model.ReserveOption.query")
    @patch("model.Owner.query")
    def test_get_all_reservation_options(self, owner_query, mock_query):
        mock_owner = Owner(id=1, username="user123")
        owner_query.filter.return_value.first.return_value = mock_owner
        mock_option1 = ReserveOption(id=1, option_type="Option A", owner=mock_owner)
        mock_option2 = ReserveOption(id=2, option_type="Option B", owner=mock_owner)
        mock_query.all.return_value = [mock_option1, mock_option2]
        response = self.app.get("/api/owner/options")
        self.assertEqual(response.status_code, 200)


class TestClientReservationListResource(BaseTestCase):
    @patch("schema.ClientReservationListSchema")
    @patch("model.ReserveOption.query")
    @patch("model.Client.query")
    @patch("model.Owner.query")
    def test_create_reservation_list(
        self, mock_query_owner, mock_query_client, mock_query_option, mock_schema
    ):
        mock_owner = Owner(id=1, username="user123")
        mock_options = ReserveOption(id=1, option_type="Option A", owner=mock_owner)
        mock_query_owner.filter.return_value.first.return_value = mock_owner
        mock_query_option.filter.return_value.first.return_value = mock_options
        mock_request_data = {
            "client": {"username": "user123"},
            "option": {
                "id": 1,
                "option_type": "Option A",
                "owner": {"id": 1, "username": "user123"},
            },
            "reserved_date": "2024-09-01T15:27:48.659128",
            "expired_in": 23,
        }

        mock_client = Client(id=1, username="user123")
        mock_query_client.filter.return_value.first.return_value = mock_client

        mock_schema_instance = mock_schema()
        mock_schema_instance.load.return_value = ClientReservationList(
            id=1,
            client=mock_client,
            option=mock_options,
            reserved_date="2024-09-01T15:27:48.659128",
            expired_date="2024-09-25T15:27:48.659128",
        )
        mock_schema.return_value = mock_schema_instance

        response = self.app.post("/api/client/options", json=mock_request_data)
        self.assertEqual(response.status_code, 200)

    @patch("model.ReserveOption.query")
    @patch("model.Client.query")
    @patch("model.Owner.query")
    @patch("model.ClientReservationList.query")
    def test_get_reservation_list(
        self, reservation_list_query, owner_query, client_query, option_query
    ):
        mock_owner = Owner(id=1, username="user123")
        owner_query.filter.return_value.first.return_value = mock_owner

        mock_options = ReserveOption(id=1, option_type="Option A", owner=mock_owner)
        option_query.filter.return_value.first.return_value = mock_options

        mock_client = Client(id=1, username="user123")
        client_query.filter.return_value.first.return_value = mock_client

        mock_reserve_list_1 = ClientReservationList(
            id=1,
            reserved_date="2024-09-01T15:27:48.659128",
            expired_date="2024-09-25T15:27:48.659128",
            option=mock_options,
            client=mock_client,
            version=1,
        )
        mock_reserve_list_2 = ClientReservationList(
            id=2,
            reserved_date="2024-10-01T15:27:48.659128",
            expired_date="2024-11-25T15:27:48.659128",
            option=mock_options,
            client=mock_client,
            version=1,
        )
        reservation_list_query.filter.return_value.first.side_effect = [
            mock_reserve_list_1,
            mock_reserve_list_2,
        ]
        response = self.app.get("/api/client/options")
        self.assertEqual(response.status_code, 200)


class TestClientReservationListIDResource(BaseTestCase):
    @patch("schema.ClientReservationListSchema")
    @patch("model.ReserveOption.query")
    @patch("model.Client.query")
    @patch("model.Owner.query")
    @patch("model.ClientReservationList.query")
    def test_get_reservation_list_by_id(
        self,
        reservation_list_query,
        owner_query,
        client_query,
        option_query,
        mock_schema,
    ):
        mock_owner = Owner(id=1, username="user123")
        owner_query.filter.return_value.first.return_value = mock_owner

        mock_options = ReserveOption(id=1, option_type="Option A", owner=mock_owner)
        option_query.filter.return_value.first.return_value = mock_options

        mock_client = Client(id=1, username="user123")
        client_query.filter.return_value.first.return_value = mock_client

        res_time = datetime.strptime(
            "2024-09-01T15:27:48.659128", "%Y-%m-%dT%H:%M:%S.%f"
        )
        exp_time = datetime.strptime(
            "2024-09-01T15:27:48.659128", "%Y-%m-%dT%H:%M:%S.%f"
        )
        mock_reserve_list_1 = ClientReservationList(
            id=1,
            reserved_date=res_time,
            expired_date=exp_time,
            option=mock_options,
            client=mock_client,
            version=1,
        )

        res_time = datetime.strptime(
            "2024-10-01T15:27:48.659128", "%Y-%m-%dT%H:%M:%S.%f"
        )
        exp_time = datetime.strptime(
            "2024-11-01T15:27:48.659128", "%Y-%m-%dT%H:%M:%S.%f"
        )
        mock_reserve_list_2 = ClientReservationList(
            id=2,
            reserved_date=res_time,
            expired_date=exp_time,
            option=mock_options,
            client=mock_client,
            version=1,
        )
        reservation_list_query.filter.return_value.first.side_effect = [
            mock_reserve_list_1,
            mock_reserve_list_2,
        ]
        response = self.app.get("/api/client/options/1")
        self.assertEqual(response.status_code, 200)

    @patch("model.ReserveOption.query")
    @patch("model.Client.query")
    @patch("model.Owner.query")
    @patch("model.ClientReservationList.query")
    def test_delete_reservation_list_by_id(
        self, reservation_list_query, owner_query, client_query, option_query
    ):
        mock_owner = Owner(id=1, username="user123")
        owner_query.filter.return_value.first.return_value = mock_owner

        mock_options = ReserveOption(id=1, option_type="Option A", owner=mock_owner)
        option_query.filter.return_value.first.return_value = mock_options

        mock_client = Client(id=1, username="user123")
        client_query.filter.return_value.first.return_value = mock_client

        res_time = datetime.strptime(
            "2024-09-01T15:27:48.659128", "%Y-%m-%dT%H:%M:%S.%f"
        )
        exp_time = datetime.strptime(
            "2024-09-01T15:27:48.659128", "%Y-%m-%dT%H:%M:%S.%f"
        )
        mock_reserve_list_1 = ClientReservationList(
            id=1,
            reserved_date=res_time,
            expired_date=exp_time,
            option=mock_options,
            client=mock_client,
            version=1,
        )

        res_time = datetime.strptime(
            "2024-10-01T15:27:48.659128", "%Y-%m-%dT%H:%M:%S.%f"
        )
        exp_time = datetime.strptime(
            "2024-11-01T15:27:48.659128", "%Y-%m-%dT%H:%M:%S.%f"
        )
        mock_reserve_list_2 = ClientReservationList(
            id=2,
            reserved_date=res_time,
            expired_date=exp_time,
            option=mock_options,
            client=mock_client,
            version=1,
        )
        reservation_list_query.filter.return_value.first.side_effect = [
            mock_reserve_list_1,
            mock_reserve_list_2,
        ]

        response = self.app.delete("/api/client/options/1")
        self.assertEqual(response.status_code, 204)
