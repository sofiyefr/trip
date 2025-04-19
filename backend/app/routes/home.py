from flask import Blueprint, request
from app.models.city_model import City
from app.extensions import db

home_bp = Blueprint('home', __name__)

@home_bp.route("/")
def home():
    return """
    Hello from the trip planner backend! 
    <a href="/cities">cities </a><br>
    """