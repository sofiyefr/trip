from app.extensions import db  

class Checkpoint(db.Model):
    __tablename__ = 'checkpoints'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    from_date = db.Column(db.String(100))
    to_date = db.Column(db.String(100))
    transport = db.Column(db.String(100))
    description = db.Column(db.String(1024))

    def __repr__(self):
        return f"<Checkpoint #{self.id} route {self.route_id} city {self.city_id}>"
