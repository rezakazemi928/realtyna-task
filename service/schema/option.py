from extensions import db, ma
from model import ReserveOption, Owner, ClientReservationList
from marshmallow import pre_load, ValidationError, fields


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
    
    class Meta:
        model = ClientReservationList
        sqla_session = db.session
        load_instance = True
