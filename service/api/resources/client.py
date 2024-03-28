from api.helpers import IdIsNotValid, UserNotFound, handle_error_response
from extensions import db
from flask import jsonify, request
from flask_restful import Resource
from model import Client
from schema import ClientSchema


class ClientResource(Resource):
    @classmethod
    def get(cls):
        # * get all the clients
        schema = ClientSchema(many=True)
        client = Client.query.all()
        return jsonify(schema.dump(client))

    @classmethod
    def post(cls):
        # * create a client
        req = request.json
        client = Client.query.filter(Client.username == req.get("username")).first()
        if client is not None:
            return handle_error_response(
                type="RequestBody",
                code=10,
                sub_code=100,
                status=409,
                msg=f"{req.get('username')} already exists.",
            )
        schema = ClientSchema(partial=True)
        client = schema.load(req)
        db.session.add(client)
        db.session.commit()

        return jsonify(schema.dump(client))


class ClientIDResource(Resource):
    @classmethod
    def get(cls, id):
        # * get a client based on id
        if id is None:
            raise IdIsNotValid("Id is required")

        client = Client.query.get(id)
        if client is None:
            raise UserNotFound("Client cannot be found")

        schema = ClientSchema(partial=True)
        return jsonify(schema.dump(client))
