from extensions import db

class ReserveOption(db.Model):
    __tablename__ = "options"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    option_type = db.Column(db.String(40), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id", ondelete="CASCADE"), nullable=False)
    
    def __repr__(self) -> str:
        return f"<{self.option_type}>"