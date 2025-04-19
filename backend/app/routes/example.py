from flask import Blueprint

example_bp = Blueprint('example', __name__)

@example_bp.route("/")
def home():
    return "Hello from the trip planner backend!"
