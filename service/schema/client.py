from extensions import ma, db
from model import Client



class ClientSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(dump_only=True)
    
    class Meta:
        model = Client
        sqla_session = db.session
        load_instance = True
