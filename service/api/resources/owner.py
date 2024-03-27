from flask_restful import Resource
from flask import request, jsonify
from model import Owner
from schema import OwnerSchema
from extensions import db
from api.helpers import handle_error_response


class OwnerResource(Resource):
    @classmethod
    def post(cls):
        req = request.json
        client = Owner.query.filter(Owner.username == req.get("username")).first()
        if client is not None:
            return handle_error_response(
                type="RequestBody",
                code=10,
                sub_code=100,
                status=409,
                msg=f"{req.get('username')} already exists."
            )
        schema = OwnerSchema(partial=True)
        client = schema.load(req)
        db.session.add(client)
        db.session.commit()
        
        return jsonify(schema.dump(client))