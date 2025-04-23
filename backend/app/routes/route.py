import random
from flask import Blueprint, abort, redirect, render_template, request
from sqlalchemy import select
from app.models.route_model import Route
from app.models.city_model import City
from app.models.checkpoint_model import Checkpoint
from app.extensions import db
from app.utils.math import distance, salesman_optimize

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


@route_bp.route("/quick_route")
def quick_route():
    return render_template('quick_route.html.j2', cities=City.query.all())


@route_bp.route("/make_quick_route")
def make_quick_route():
    name = request.values.get("name")
    route = Route(name=name, description="")
    db.session.add(route)
    db.session.commit()

    cities = request.values.getlist("cities")
    random.shuffle(cities)
    cities.append( cities[0] )

    for idx, city_id in enumerate(cities):
        city = Checkpoint(
            city_id=city_id, 
            route_id=route.id,
            index=idx, 
            from_date = "",
            to_date = "",
            transport = "",
            description = "")
        db.session.add(city)
    db.session.commit()
    print("Route id = ", route.id)
    return redirect(f'salesman/{route.id}')


@route_bp.route("/salesman/<id>")
def salesman(id):
    route = Route.query.get(id)
    if not route: abort(404)
    cities = City.query.all()
    checkpooints_stmt = select(Checkpoint).where(Checkpoint.route_id == route.id).order_by(Checkpoint.index)
    checkpoints = [checkpoint for checkpoint in db.session.scalars(checkpooints_stmt)]
    prev = None
    totall_dist = 0
    for checkpoint in checkpoints:
        checkpoint.city = City.query.get(checkpoint.city_id)
        if prev:
            dist = distance(checkpoint.city, prev.city)
            totall_dist += dist
            prev.dist = int(dist + .5)
        prev = checkpoint
    route.dist = int(totall_dist + .5)
    return render_template('salesman.html.j2', route=route, cities=cities, checkpoints=checkpoints)


@route_bp.route("/route/<id>/shuffle")
def route_shuffle(id):
    checkpooints_stmt = select(Checkpoint).where(Checkpoint.route_id == id).order_by(Checkpoint.index)
    checkpoints = [checkpoint for checkpoint in db.session.scalars(checkpooints_stmt)]
    prev = None
    totall_dist = 0
    for checkpoint in checkpoints:
        checkpoint.city = City.query.get(checkpoint.city_id)
        if prev:
            dist = distance(checkpoint.city, prev.city)
            totall_dist += dist
            prev.dist = int(dist + .5)
        prev = checkpoint
    first = checkpoints[0]
    checkpoints = checkpoints[1:]
    random.shuffle(checkpoints)
    first.city_id = checkpoints[0].city_id
    checkpoints.append(first)
    for idx, checkpoint in enumerate( checkpoints):
        checkpoint.index = idx
    db.session.commit()
    return redirect(f'/salesman/{id}')


@route_bp.route("/route/<id>/optimize")
def route_optimize(id):
    checkpooints_stmt = select(Checkpoint).where(Checkpoint.route_id == id).order_by(Checkpoint.index)
    checkpoints = [checkpoint for checkpoint in db.session.scalars(checkpooints_stmt)]
    prev = None
    totall_dist = 0
    for checkpoint in checkpoints:
        checkpoint.city = City.query.get(checkpoint.city_id)
        if prev:
            dist = distance(checkpoint.city, prev.city)
            totall_dist += dist
            prev.dist = int(dist + .5)
        prev = checkpoint

    salesman_optimize(checkpoints)

    for idx, checkpoint in enumerate( checkpoints):
        checkpoint.index = idx
    db.session.commit()
    return redirect(f'/salesman/{id}')


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
