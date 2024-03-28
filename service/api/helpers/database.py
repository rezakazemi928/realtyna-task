from datetime import datetime
from model import ClientReservationList

def check_reserved_date(input_time:datetime, id:int=None):
    matching_reservations = ClientReservationList.query.filter(
        ClientReservationList.reserved_date <= input_time,
        ClientReservationList.expired_date >= input_time,
        ClientReservationList.id == id
    ).first()
    return matching_reservations