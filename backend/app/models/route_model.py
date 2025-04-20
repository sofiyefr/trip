from app.extensions import db  

class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024))

    def __repr__(self):
        return f"<Route #{self.id} {self.name}>"
