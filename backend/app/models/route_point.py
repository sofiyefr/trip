from app import db

class RoutePoint(db.Model):
    __tablename__ = 'route_points'
    
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id', ondelete='CASCADE'), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    transportation_type = db.Column(db.String(50))
    order_number = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'city': self.city,
            'transportation_type': self.transportation_type,
            'order_number': self.order_number
        } 