from flask import Blueprint
from flask_restful import Api

from api.resources import ClientResource, ClientResourceID, OwnerResource, ReservationOptionResource


blueprint = Blueprint("realtyna", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(ClientResource, "/client", endpoint="client_resource")
api.add_resource(ClientResourceID, "/client/<int:id>", endpoint="client_resource_with_id")
api.add_resource(OwnerResource, "/owner", endpoint="owner_resource")
api.add_resource(ReservationOptionResource, "/owner/options", endpoint="owner_options")