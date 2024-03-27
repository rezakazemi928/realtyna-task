from flask import Blueprint
from flask_restful import Api

from api.resources import ClientResource


blueprint = Blueprint("realtyna", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(ClientResource, "/client", endpoint="client_resource")