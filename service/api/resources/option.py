from api.helpers import InvalidRequestArgs, ReservationNotFound
from extensions import db
from flask import Response, jsonify, request
from flask_restful import Resource
from model import ClientReservationList, ReserveOption
from schema import (
    ClientReservationListSchema,
    ClientReservationListUpdateSchema,
    ReserveOptionSchema,
)


class ReservationOptionResource(Resource):
    @classmethod
    def post(cls):
        # * create a reservation option
        req = request.json
        schema = ReserveOptionSchema(partial=True)
        option = schema.load(req)
        db.session.add(option)
        db.session.commit()

        return jsonify(schema.dump(option))

    def get(cls):
        options = ReserveOption.query.all()
        schema = ReserveOptionSchema(many=True)
        return jsonify(schema.dump(options))


class ClientReservationListResource(Resource):
    @classmethod
    def post(cls):
        req = request.json
        schema = ClientReservationListSchema(partial=True)
        reservation_list = schema.load(req)
        db.session.add(reservation_list)
        db.session.commit()
        return jsonify(schema.dump(reservation_list))

    @classmethod
    def get(cls):
        schema = ClientReservationListSchema(many=True)
        reservations_list = ClientReservationList.query.all()
        return jsonify(schema.dump(reservations_list))


class ClientReservationListIDResource(Resource):
    @classmethod
    def get(cls, id):
        reservation_list = ClientReservationList.query.get(id)
        if reservation_list is None:
            raise ReservationNotFound("No reservation had found based on this id")

        schema = ClientReservationListSchema(partial=True)
        return jsonify(schema.dump(reservation_list))

    @classmethod
    def put(cls, id):
        args = request.args
        req = request.json
        version = args.get("version")
        if version is None:
            raise InvalidRequestArgs("row version is not valid")

        reservation_list = ClientReservationList.query.filter(
            ClientReservationList.id == id, ClientReservationList.version == version
        ).first()
        if reservation_list is None:
            raise ReservationNotFound("No reservation has been found.")

        req["id"] = id
        reservation_list.reserved_date = None
        reservation_list.expired_date = None
        db.session.flush()

        schema = ClientReservationListUpdateSchema(partial=True)
        reservation_list = schema.load(req, instance=reservation_list)
        reservation_list.version += 1
        db.session.commit()
        return jsonify(schema.dump(reservation_list))

    @classmethod
    def delete(cls, id):
        reservation_list = ClientReservationList.query.get(id)
        if reservation_list is None:
            raise ReservationNotFound("No reservation has been found.")

        ClientReservationList.query.filter(ClientReservationList.id == id).delete()
        db.session.commit()
        return Response(None, status=204, mimetype="application/json")
