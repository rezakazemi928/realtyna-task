from flask import Blueprint
from flask_restful import Api


blueprint = Blueprint("realtyna", __name__, url_prefix="/api")
api = Api(blueprint)