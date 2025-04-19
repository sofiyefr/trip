from flask import Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route("/")
def home():
    return """
    Hello from the trip planner backend! 
    <a href="/cities">cities </a><br>
    """