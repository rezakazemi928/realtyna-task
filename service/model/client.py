from extensions import db
from sqlalchemy import func


class Client(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True)
    registered_date = db.Column(
        db.DateTime(timezone=True), nullable=False, default=func.now()
    )
    def __repr__(self) -> str:
        return f"<{self.username}>"
    