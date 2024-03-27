from extensions import db, ma
from model import ReserveOption


class ReserveOptionSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(dump_only=True)
    option_type = ma.String(required=True)
    owner_id = ma.Integer(required=True)
    
    class  Meta:
        model = ReserveOption
        sqla_session = db.session
        load_instance = True
        
    