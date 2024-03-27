from extensions import db
from sqlalchemy import func


class Owner(db.Model):
    __tablename__ = "owner"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True)
    registered_date = db.Column(
        db.DateTime(timezone=True), nullable=False, default=func.now()
    )
    
    def __repr__(self) -> str:
        return f"<{self.username}>"
    