from datetime import datetime
from model import ClientReservationList

def check_reserved_date(input_time:datetime):
    # input_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    matching_reservations = ClientReservationList.query.filter(
            ClientReservationList.reserved_date <= input_time,
            ClientReservationList.expired_date >= input_time
        ).first()
    return matching_reservations