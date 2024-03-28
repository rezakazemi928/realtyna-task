from datetime import datetime, timedelta

from api.helpers import check_reserved_date
from extensions import db, ma
from marshmallow import ValidationError, fields, pre_load
from model import Client, ClientReservationList, Owner, ReserveOption


class ReservationOptionSchemaBase(ma.SQLAlchemyAutoSchema):
    option_type = ma.String(required=True)
    owner = fields.Nested("OwnerSchemaBase", only=("id", "username"), required=True)

    class Meta:
        model = ReserveOption
        sqla_session = db.session
        load_instance = True

    @pre_load
    def validate_request(self, req, **kwargs):
        owner = Owner.query.filter(
            Owner.username == req["owner"]["username"], Owner.id == req["owner"]["id"]
        ).first()
        if owner is None:
            raise ValidationError("owner cannot be found")

        return req


class ReserveOptionSchema(ReservationOptionSchemaBase):
    id = ma.Integer(dump_only=True)


class ClientReservationListSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(dump_only=True)
    client = fields.Nested("ClientSchemaBase", only=("username", "id"), required=True)
    option = fields.Nested("ReservationOptionSchemaBase", required=True)
    reserved_date = ma.DateTime(required=True)
    expired_date = ma.DateTime(required=True)
    expired_in = ma.Integer(required=True, load_only=True)

    class Meta:
        model = ClientReservationList
        sqla_session = db.session
        load_instance = True

    @pre_load
    def validate_request(self, req, **kwargs):
        client = Client.query.filter(
            Client.username == req["client"]["username"]
        ).first()
        if client is None:
            raise ValidationError("Client is not valid for reservation")

        req["client"]["id"] = client.id

        option = ReserveOption.query.get(req["option"]["id"])
        if option is None:
            raise ValidationError("No option has found for reservation.")

        # *Get the current datetime in UTC
        current_datetime_utc = datetime.utcnow()

        # * change the time format into ISO 8061
        # * convert it to the time object in order to do the calculations and searching
        reserved_datetime = datetime.strptime(
            req["reserved_date"], "%Y-%m-%dT%H:%M:%S.%f"
        )
        if reserved_datetime < current_datetime_utc:
            raise ValidationError("not a valid reserved date")

        is_reserved = check_reserved_date(
            input_time=reserved_datetime, id=req["option"]["id"]
        )
        if is_reserved is not None:
            raise ValidationError("Already reserved")

        req["expired_date"] = (
            reserved_datetime + timedelta(days=req["expired_in"])
        ).strftime("%Y-%m-%dT%H:%M:%S.%f")
        del req["expired_in"]

        return req


class ClientReservationListUpdateSchema(ClientReservationListSchema):
    id = ma.Integer(required=True)
    client = fields.Nested(
        "ClientSchemaBase", only=("id", "username"), required=True, dump_only=True
    )
    option = fields.Nested("ReservationOptionSchemaBase", required=True, dump_only=True)

    @pre_load
    def validate_request(self, req, **kwargs):
        # *Get the current datetime in UTC
        current_datetime_utc = datetime.utcnow() - timedelta(days=1)

        reserved_datetime = datetime.strptime(
            req["reserved_date"], "%Y-%m-%dT%H:%M:%S.%f"
        )
        if reserved_datetime < current_datetime_utc:
            raise ValidationError("not a valid reserved date")

        is_reserved = check_reserved_date(
            input_time=reserved_datetime, id=req["option"]["id"]
        )
        if is_reserved is not None:
            raise ValidationError("Already reserved")

        req["expired_date"] = (
            reserved_datetime + timedelta(days=req["expired_in"])
        ).strftime("%Y-%m-%dT%H:%M:%S.%f")
        del req["expired_in"]

        return req
