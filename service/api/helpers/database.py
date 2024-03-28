from datetime import datetime
from typing import Union

from model import Client, ClientReservationList


def check_reserved_date(
    input_time: datetime, id: int
) -> Union[None, ClientReservationList]:
    """check if the option already reserved in database.

    Args:
        input_time (datetime): time object for searching
        id (int): reservation id

    """
    matching_reservations = ClientReservationList.query.filter(
        ClientReservationList.reserved_date <= input_time,
        ClientReservationList.expired_date >= input_time,
        ClientReservationList.id == id,
    ).first()
    return matching_reservations


class ReservationListSearch:
    def __init__(self, args, db) -> None:
        self.args = args
        self.db = db

    def set_base_query(self):
        self.query = (
            self.db.session.query(ClientReservationList)
            .select_from(Client)
            .outerjoin(
                ClientReservationList, ClientReservationList.client_id == Client.id
            )
        )

    def filter_reservations_by_username(self):
        if self.args.get("username"):
            username = self.args.get("username")
            self.query = self.query.filter(Client.username.ilike(f"%{username}%"))

    def filter_by_timeline(self):
        started_date = self.args.get("started_date")
        end_date = self.args.get("end_date")
        if started_date is not None and end_date is not None:
            started_date = datetime.strptime(started_date, "%Y-%m-%dT%H:%M:%S.%f")
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%f")
            self.query = self.query.filter(
                (ClientReservationList.reserved_date > end_date)
                | (ClientReservationList.expired_date < started_date)
            )

        return self.query
