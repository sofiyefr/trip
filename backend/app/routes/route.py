from flask import Blueprint, abort, redirect, render_template, request
from sqlalchemy import select
from app.models.route_model import Route
from app.models.city_model import City
from app.models.checkpoint_model import Checkpoint
from app.extensions import db

route_bp = Blueprint('routes', __name__)

transports = [
    "🚌 bus",
    "🚆 train",
    "🛫 plane",
    "🚗 car",
    "🚲 bike",
    "🚕 taxi",
    "🚢 ship"
]

@route_bp.route("/routes")
def list():
    return render_template('routes.html.j2', routes=Route.query.all())

@route_bp.route("/route/<id>")
def show(id):
    route = Route.query.get(id)
    if not route: abort(404)
    cities = City.query.all()
    checkpooints_stmt = select(Checkpoint).where(Checkpoint.route_id == route.id)
    checkpoints = [checkpoint for checkpoint in db.session.scalars(checkpooints_stmt)]
    for checkpoint in checkpoints:
        checkpoint.city = City.query.get(checkpoint.city_id)
    #checkpoints = db.session.scalars(checkpooints_stmt)
    return render_template('route.html.j2', route=route, cities=cities, checkpoints=checkpoints, transports=transports)

@route_bp.route("/route/add", methods=["POST", "GET"])
def add():
    name = request.values.get("name")
    description = request.values.get("description")

    route = Route(
        name=name,
        description=description)

    db.session.add(route)
    db.session.commit()
    
    return redirect(f"/route/{route.id}")


@route_bp.route("/route/<id>/edit", methods=["POST", "GET"])
def edit(id):
    name = request.values.get("name")
    description = request.values.get("description")

    route = Route.query.get(id)
    if not route: abort(404)

    route.name = name
    route.description = description
    db.session.commit()

    return redirect(f"/route/{route.id}")

@route_bp.route("/route/<id>/delete", methods=["POST", "GET"])
def delete(id):
    route = Route.query.get(id)
    if not route: abort(404)
    db.session.delete(route)
    db.session.commit()
    return redirect("/routes")
    
    
@route_bp.route("/route_as_json/<id>")
def as_json(id):
    route = Route.query.get(id)
    if not route: abort(404)
    route_dict = {
        "id": route.id,
        "name": route.name,
        "description": route.description,
    }
    return f'{{"route":{route_dict}}}'
