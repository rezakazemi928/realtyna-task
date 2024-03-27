from flask_restful import Resource
from flask import request, jsonify
from schema import ReserveOptionSchema
from extensions import db


class ReservationOptionResource(Resource):
    @classmethod
    def post(cls):
        req = request.json
        schema = ReserveOptionSchema(partial=True)
        option = schema.load(req)
        db.session.add(option)
        db.session.commit()
        
        return jsonify(schema.dump(option))
        