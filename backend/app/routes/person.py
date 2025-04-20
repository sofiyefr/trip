from flask import Blueprint, abort, redirect, render_template, request
from app.models.person_model import Person
from app.extensions import db

person_bp = Blueprint('persons', __name__)

@person_bp.route("/persons")
def list():
    return render_template('persons.html.j2', persons=Person.query.all())

@person_bp.route("/person/add", methods=["POST", "GET"])
def add():
    name = request.values.get("name")
    birthday = request.values.get("birthday")

    person = Person(name=name, birthday=birthday)
    db.session.add(person)
    db.session.commit()
    
    return redirect("/persons")


@person_bp.route("/person/<id>/edit", methods=["POST", "GET"])
def edit(id):
    name = request.values.get("name")
    birthday = request.values.get("birthday")

    person = Person.query.get(id)
    if not person: abort(404)

    person.name = name
    person.birthday = birthday
    db.session.commit()
    return redirect("/persons")

@person_bp.route("/person/<id>/delete", methods=["POST", "GET"])
def delete(id):
    person = Person.query.get(id)
    if not person: abort(404)
    db.session.delete(person)
    db.session.commit()
    return redirect("/persons")
    
    
@person_bp.route("/persons_as_json")
def as_json():
    list = ",".join([
        f'{{"id"={person.id}, "name"="{person.name}", "birthday"={person.birthday}}}'
        for person in Person.query.all()
    ])
    return f'{{"persons":[{list}]}}'
