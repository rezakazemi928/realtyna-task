from extensions import ma, db
from model import Owner



class OwnerSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(dump_only=True)
    
    class Meta:
        model = Owner
        sqla_session = db.session
        load_instance = True
