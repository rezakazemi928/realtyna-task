from datetime import datetime
from typing import Union

from model import ClientReservationList


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
