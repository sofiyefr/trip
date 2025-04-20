from app.extensions import db  

class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024))
    from_time = db.Column(db.String(100))
    from_city = db.Column(db.Integer)
    to_time = db.Column(db.String(100))
    to_city = db.Column(db.Integer)
    transport = db.Column(db.String(100))

    def __repr__(self):
        return f"<Route #{self.id} {self.name} ({self.from_city} -> {self.to_city})>"
