from datetime import datetime, timedelta
from marshmallow import pre_load, ValidationError, fields
from extensions import db, ma
from model import ReserveOption, Owner, ClientReservationList
from api.helpers import check_reserved_date


class ReserveOptionSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(dump_only=True)
    option_type = ma.String(required=True)
    owner = fields.Nested("OwnerSchemaBase", only=("id", "username"), required=True)
    
    class  Meta:
        model = ReserveOption
        sqla_session = db.session
        load_instance = True
    
    @pre_load
    def validate_request(self, req, **kwargs):
        owner = Owner.query.get(req["owner"]["id"])
        if owner is None:
            raise ValidationError("owner cannot be found")
        
        return req
    

class ClientReservationListSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(dump_only=True)
    client = fields.Nested("ClientSchema", only=("id", "username"), required=True)
    option = fields.Nested("ReserveOptionSchema", required=True)
    reserved_date = ma.DateTime(required=True)
    expired_in = ma.Integer(required=True, load_only=True)
    
    class Meta:
        model = ClientReservationList
        sqla_session = db.session
        load_instance = True
        
    @pre_load
    def validate_request(self, req, **kwargs):
        # *Get the current datetime in UTC
        current_datetime_utc = datetime.now(datetime.timezone.utc)
        # *Convert to ISO 8601 format
        reserved_datetime = datetime.strptime(req["reserved_date"], "%Y-%m-%dT%H:%M:%SZ")
        if reserved_datetime < current_datetime_utc:
            raise ValidationError("not a valid reserved date")
        
        if check_reserved_date(input_time=reserved_datetime) is not None:
            raise ValidationError("Already reserved")
        
        req["expired_date"] = reserved_datetime + timedelta(days=req["expired_in"])
        del req["expired_in"]
        
        return req
        
