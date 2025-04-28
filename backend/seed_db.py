from app import db, create_app
from app.models.user import User
from app.models.trip import Trip
from app.models.route_point import RoutePoint
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def seed_database():
    # Create test user
    test_user = User(
        username='test_user',
        email='test@example.com',
        password_hash=generate_password_hash('password123')
    )
    db.session.add(test_user)
    db.session.commit()

    # Create test trip
    test_trip = Trip(
        user_id=test_user.id,
        title='Подорож до моря',
        description='Літня відпустка на морі',
        start_date=datetime.now().date(),
        end_date=(datetime.now() + timedelta(days=7)).date(),
        budget=15000.0,
        is_public=True
    )
    db.session.add(test_trip)
    db.session.commit()

    # Create route points
    route_points = [
        RoutePoint(
            trip_id=test_trip.id,
            city='Львів',
            order_number=1
        ),
        RoutePoint(
            trip_id=test_trip.id,
            city='Київ',
            transportation_type='train',
            order_number=2
        ),
        RoutePoint(
            trip_id=test_trip.id,
            city='Одеса',
            transportation_type='bus',
            order_number=3
        )
    ]
    
    for point in route_points:
        db.session.add(point)
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_database()
        print("Database seeded successfully!") 