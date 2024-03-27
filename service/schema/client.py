from extensions import ma, db
from model import Client


class ClientSchemaBase(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        sqla_session = db.session
        load_instance = True

class ClientSchema(ClientSchemaBase):
    id = ma.Integer(dump_only=True)
    

