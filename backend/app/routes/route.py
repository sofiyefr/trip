from flask import Blueprint, abort, redirect, render_template, request
from sqlalchemy import select
from app.models.route_model import Route
from app.extensions import db

route_bp = Blueprint('routes', __name__)

@route_bp.route("/routes")
def list():
    stmt = select(Route).where(Route.parent_id == None)
    root_routes = db.session.scalars(stmt)
    return render_template('routes.html.j2', routes=root_routes)

@route_bp.route("/route/<id>")
def show(id):
    route = Route.query.get(id)
    if not route: abort(404)
    return render_template('route.html.j2', route=route)

@route_bp.route("/route/add", methods=["POST", "GET"])
def add():
    parent_id = request.values.get("parent_id")
    name = request.values.get("name")
    description = request.values.get("description")

    from_time = request.values.get("from_time")
    from_city = request.values.get("from_city")
    to_time = request.values.get("to_time")
    to_city = request.values.get("to_city")
    transport = request.values.get("transport")

    route = Route(
        parent_id=parent_id,
        name=name,
        description=description,
        from_time=from_time,
        from_city=from_city,
        to_time=to_time,
        to_city=to_city,
        transport=transport
    )

    db.session.add(route)
    db.session.commit()
    
    return redirect(f"/route/{route.id}")


@route_bp.route("/route/<id>/edit", methods=["POST", "GET"])
def edit(id):
    parent_id = request.values.get("parent_id")
    name = request.values.get("name")
    description = request.values.get("description")
    birthday = request.values.get("birthday")

    from_time = request.values.get("from_time")
    from_city = request.values.get("from_city")
    to_time = request.values.get("to_time")
    to_city = request.values.get("to_city")
    transport = request.values.get("transport")

    route = Route.query.get(id)
    if not route: abort(404)

    route.parent_id = parent_id
    route.name = name
    route.description = description
    route.birthday = birthday
    route.from_time = from_time
    route.from_city = from_city
    route.to_time = to_time
    route.to_city = to_city
    route.transport = transport
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
        "parent_id": route.parent_id,
        "name": route.name,
        "description": route.description,
        "birthday": route.birthday,
        "from_time": route.from_time,
        "from_city": route.from_city,
        "to_time": route.to_time,
        "to_city": route.to_city,
        "transport": route.transport
    }
    return f'{{"route":{route_dict}}}'
