from extensions import db, ma
from model import Owner


class OwnerSchemaBase(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
        sqla_session = db.session
        load_instance = True


class OwnerSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(dump_only=True)

    class Meta:
        model = Owner
        sqla_session = db.session
        load_instance = True
