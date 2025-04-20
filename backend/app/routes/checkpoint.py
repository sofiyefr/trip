from flask import Blueprint, abort, redirect, render_template, request
from sqlalchemy import select
from app.models.route_model import Route
from app.models.city_model import City
from app.models.checkpoint_model import Checkpoint
from app.extensions import db

checkpoint_bp = Blueprint('checkpoints', __name__)

@checkpoint_bp.route("/checkpoint/add", methods=["POST", "GET"])
def add():
    route_id = request.values.get("route_id")
    city_id = request.values.get("city_id")
    date = request.values.get("date")
    transport = request.values.get("transport")
    description = request.values.get("description")

    checkpoint = Checkpoint(
        route_id = route_id,
        city_id = city_id,
        from_date = date,
        to_date = date,
        transport = transport,
        description = description)

    db.session.add(checkpoint)
    db.session.commit()
    
    return redirect(f"/route/{route_id}")


@checkpoint_bp.route("/checkpoint/<id>/edit", methods=["POST", "GET"])
def edit(id):
    city_id = request.values.get("city_id")
    from_date = request.values.get("from_date")
    to_date = request.values.get("to_date")
    transport = request.values.get("transport")
    description = request.values.get("description")

    checkpoint = Checkpoint.query.get(id)
    if not checkpoint: abort(404)

    checkpoint.city_id = city_id
    checkpoint.from_date = from_date
    checkpoint.to_date = to_date
    checkpoint.transport = transport
    checkpoint.description = description
    db.session.commit()

    return redirect(f"/route/{checkpoint.route_id}")

@checkpoint_bp.route("/checkpoint/<id>/delete", methods=["POST", "GET"])
def delete(id):
    checkpoint = Checkpoint.query.get(id)
    route_id = checkpoint.route_id
    if not checkpoint: abort(404)
    db.session.delete(checkpoint)
    db.session.commit()
    return redirect(f"/route/{checkpoint.route_id}")
