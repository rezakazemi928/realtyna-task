"""routes"""


from api.resources import (
    ClientIDResource,
    ClientReservationListIDResource,
    ClientReservationListResource,
    ClientResource,
    OwnerResource,
    ReservationOptionResource,
)
from flask import Blueprint
from flask_restful import Api

blueprint = Blueprint("realtyna", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(ClientResource, "/client", endpoint="client_resource")
api.add_resource(
    ClientIDResource, "/client/<int:id>", endpoint="client_resource_with_id"
)
api.add_resource(OwnerResource, "/owner", endpoint="owner_resource")
api.add_resource(ReservationOptionResource, "/owner/options", endpoint="owner_options")
api.add_resource(
    ClientReservationListResource,
    "/client/options",
    endpoint="client_reservation_list_resource",
)
api.add_resource(
    ClientReservationListIDResource,
    "/client/options/<int:id>",
    endpoint="client_reservation_list_with_id_resource",
)
