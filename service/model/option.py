from extensions import db


class ReserveOption(db.Model):
    __tablename__ = "options"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    option_type = db.Column(db.String(40), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id", ondelete="CASCADE"), nullable=False)
    owner = db.relationship(
        "Owner",
        backref="owner",
        lazy=True,
        passive_deletes=True,
    )
    def __repr__(self) -> str:
        return f"<{self.option_type}>"
    

class ClientReservationList(db.Model):
    __tablename__ = "reservation_list"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey("options.id", ondelete="CASCADE"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    reserved_date = db.Column(db.DateTime(timezone=True), nullable=False)
    expired_date = db.Column(db.DateTime(timezone=True), nullable=False)
    currently_available = db.Column(db.Boolean, default=False, nullable=False)
    client = db.relationship(
        "Client",
        backref="client",
        lazy=True,
        passive_deletes=True,
    )
    option = db.relationship(
        "ReserveOption",
        backref="option",
        lazy=True,
        passive_deletes=True,
    )
    
    def __repr__(self) -> str:
        return f"<{self.id}>"