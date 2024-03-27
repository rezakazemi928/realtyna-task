from flask_restful import Resource
from flask import request, jsonify, Response
from schema import ReserveOptionSchema, ClientReservationListSchema, ClientReservationListUpdateSchema
from extensions import db
from model import ClientReservationList
from api.helpers import ReservationNotFound


class ReservationOptionResource(Resource):
    @classmethod
    def post(cls):
        req = request.json
        schema = ReserveOptionSchema(partial=True)
        option = schema.load(req)
        db.session.add(option)
        db.session.commit()
        
        return jsonify(schema.dump(option))
        
        
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
        req = request.json
        req["id"] = id
        reservation_list = ClientReservationList.query.get(id)
        if reservation_list is None:
            raise ReservationNotFound("No reservation has been found.")
        
        schema = ClientReservationListUpdateSchema(partial=True)
        reservation_list = schema.load(req, instance=reservation_list)
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