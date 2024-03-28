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


def filter_reservations_by_username(username: str, db):
    query = (
        db.session.query(ClientReservationList)
        .select_from(Client)
        .outerjoin(ClientReservationList, ClientReservationList.client_id == Client.id)
        .filter(Client.username.ilike(f"%{username}%"))
    )
    return query
