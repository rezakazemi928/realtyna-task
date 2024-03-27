from extensions import db

class ReserveOption(db.Model):
    __tablename__ = "options"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    option_type = db.Column(db.String(40), nullable=False)
    currently_available = db.Column(db.Boolean, nullable=False, default=True)
    reserved_date = db.Column(db.DateTime(timezone=True), nullable=True)
    expired_date = db.Column(db.DateTime(timezone=True), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id", ondelete="SET NULL"))
    version = db.Column(db.Integer, nullable=False, default=1)
    
    def __repr__(self) -> str:
        return f"<{self.option_type}>"