from flask import Flask, url_for
from app.routes.home import home_bp
from app.routes.city import city_bp
from app.routes.person import person_bp
from app.routes.route import route_bp
from app.routes.checkpoint import checkpoint_bp
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db  
# Initialize the database
#db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    print("__name__", __name__)
    print("app.static_url_path", app.static_url_path)
    app.config.from_object('config.Config')

    db.init_app(app)  # Properly initialize with app

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(city_bp)
    app.register_blueprint(person_bp)
    app.register_blueprint(route_bp)
    app.register_blueprint(checkpoint_bp)

    # Create tables if they don't exist
    with app.app_context():
        # Import after init_app
        from app.models.city_model import City  
        from app.models.person_model import Person
        from app.models.route_model import Route
        from app.models.checkpoint_model import Checkpoint
        db.create_all()
        # Print the database URI to verify the connection
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    return app