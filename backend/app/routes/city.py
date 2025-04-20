from flask import Blueprint, abort, redirect, render_template, request
from app.models.city_model import City
from app.extensions import db

city_bp = Blueprint('city', __name__)

@city_bp.route("/cities")
def list():
    return render_template('cities.html.j2', cities=City.query.all())


@city_bp.route("/city/add", methods=["POST", "GET"])
def add():
    name = request.values.get("name")
    latitude = request.values.get("latitude")
    longitude = request.values.get("longitude")

    city = City(name=name, latitude=latitude, longitude=longitude)
    db.session.add(city)
    db.session.commit()
    
    return redirect("/cities")


@city_bp.route("/city/<id>/edit", methods=["POST", "GET"])
def edit(id):
    name = request.values.get("name")
    latitude = request.values.get("latitude")
    longitude = request.values.get("longitude")

    city = City.query.get(id)
    if not city: abort(404)
    
    city.name = name
    city.latitude = latitude
    city.longitude = longitude
    db.session.commit()
    return redirect("/cities")


@city_bp.route("/city/<id>/delete", methods=["POST", "GET"])
def delete(id):
    city = City.query.get(id)
    if not city: abort(404)

    db.session.delete(city)
    db.session.commit()
    return redirect("/cities")

    
@city_bp.route("/cities_as_json")
def as_json():
    list = ",".join([
        f'{{"id"={city.id}, "name"="{city.name}", "latitude"={city.latitude}, "longitude"={city.longitude}}}'
        for city in City.query.all()
    ])
    return f'{{"cities":[{list}]}}'
