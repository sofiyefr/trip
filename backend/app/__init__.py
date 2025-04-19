from flask import Flask
from app.routes.home import home_bp
from app.routes.city import city_bp
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db  
# Initialize the database
#db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)  # Properly initialize with app

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(city_bp)

    # Create tables if they don't exist
    with app.app_context():
        from app.models.city_model import City  # Import after init_app
        db.create_all()
        # Print the database URI to verify the connection
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    return app