from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import db
from app.models.user import User
from app.models.trip import Trip
from app.models.route_point import RoutePoint

def seed_database():
    # Clear existing data
    db.session.query(RoutePoint).delete()
    db.session.query(Trip).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create users
    users = [
        User(
            username="sofia_travel",
            email="sofia@example.com",
            password_hash=generate_password_hash("password123")
        ),
        User(
            username="john_doe",
            email="john@example.com",
            password_hash=generate_password_hash("password123")
        ),
        User(
            username="maria_adventures",
            email="maria@example.com",
            password_hash=generate_password_hash("password123")
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    # Create trips
    current_date = datetime.utcnow()
    trips = [
        Trip(
            user_id=users[0].id,
            title="Подорож Україною",
            description="Захоплююча подорож визначними місцями України",
            start_date=current_date + timedelta(days=10),
            end_date=current_date + timedelta(days=20),
            budget=15000,
            is_public=True,
            transportation_type="Потяг",
            departure_city="Київ",
            destination_city="Львів"
        ),
        Trip(
            user_id=users[1].id,
            title="Європейський тур",
            description="Подорож столицями Європи",
            start_date=current_date + timedelta(days=30),
            end_date=current_date + timedelta(days=45),
            budget=50000,
            is_public=True,
            transportation_type="Літак",
            departure_city="Київ",
            destination_city="Париж"
        ),
        Trip(
            user_id=users[2].id,
            title="Вихідні на морі",
            description="Відпочинок на узбережжі",
            start_date=current_date + timedelta(days=5),
            end_date=current_date + timedelta(days=7),
            budget=8000,
            is_public=False,
            transportation_type="Автомобіль",
            departure_city="Київ",
            destination_city="Одеса"
        )
    ]
    db.session.add_all(trips)
    db.session.commit()

    # Create route points
    route_points = [
        # Для першої подорожі
        RoutePoint(
            trip_id=trips[0].id,
            city="Київ",
            order_number=1
        ),
        RoutePoint(
            trip_id=trips[0].id,
            city="Вінниця",
            order_number=2
        ),
        RoutePoint(
            trip_id=trips[0].id,
            city="Львів",
            order_number=3
        ),
        # Для другої подорожі
        RoutePoint(
            trip_id=trips[1].id,
            city="Київ",
            order_number=1
        ),
        RoutePoint(
            trip_id=trips[1].id,
            city="Варшава",
            order_number=2
        ),
        RoutePoint(
            trip_id=trips[1].id,
            city="Париж",
            order_number=3
        ),
        # Для третьої подорожі
        RoutePoint(
            trip_id=trips[2].id,
            city="Київ",
            order_number=1
        ),
        RoutePoint(
            trip_id=trips[2].id,
            city="Умань",
            order_number=2
        ),
        RoutePoint(
            trip_id=trips[2].id,
            city="Одеса",
            order_number=3
        )
    ]
    db.session.add_all(route_points)
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database() 