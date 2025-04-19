from flask import Flask
from app.routes.example import example_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Register blueprints
    app.register_blueprint(example_bp)

    return app