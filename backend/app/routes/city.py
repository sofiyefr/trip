from flask import Blueprint, request
from app.models.city_model import City
from app.extensions import db

city_bp = Blueprint('city', __name__)

@city_bp.route("/cities")
def list():

    list = "".join([
        f'''
        <tr>
        <td>{city.id}</td>
        <form action=edit_city>
        <input type="hidden" name="id" value="{city.id}">
        <td><input type="text" name="name" value="{city.name}"></td>
        <td><input type="text" name="latitude" value="{city.latitude}"></td>
        <td><input type="text" name="longitude" value="{city.longitude}"></td>
        <td><input type="submit" value="Update"></td>
        </form>
        <form action=delete_city>
        <input type="hidden" name="id" value="{city.id}">
        <td><input type="submit" value="Delete"></td>
        </form>
        <form action=copy_city>
        <input type="hidden" name="id" value="{city.id}">
        <td><input type="submit" value="Copy"></td>
        </form>
        <td> <a href="https://www.google.com/maps?q={city.latitude},{city.longitude}" target="_blank">
            {city.latitude},{city.longitude}</a></td>
        <td><a href="https://www.google.com/maps?q={city.name}" target="_blank">
            {city.name}</a></td>
        </tr>
        '''
        for city in City.query.all()
    ])

    add_city = """
    <tr>
        <td></td>
        <form action=add_city>
        <td><input type="text" name="name" value="name"></td>
        <td><input type="text" name="latitude" value="0"></td>
        <td><input type="text" name="longitude" value="0"></td>
        <td><input type="submit" value="Add"></td>
        </form>
    """

    return f'''
    List of cities: <br>
    <table>
    {list}
    {add_city}
    </table> <br>
    <a href="/">Go back </a>
    '''

@city_bp.route("/add_city", methods=["POST", "GET"])
def add():
    name = request.values.get("name")
    latitude = request.values.get("latitude")
    longitude = request.values.get("longitude")

    city = City(name=name, latitude=latitude, longitude=longitude)
    db.session.add(city)
    db.session.commit()
    
    return f'City {name} added successfully! <br>' + list()


@city_bp.route("/edit_city", methods=["POST", "GET"])
def edit():
    id = request.values.get("id")
    name = request.values.get("name")
    latitude = request.values.get("latitude")
    longitude = request.values.get("longitude")

    city = City.query.get(id)
    if city:
        city.name = name
        city.latitude = latitude
        city.longitude = longitude
        db.session.commit()
        return f'City {name} updated successfully! <br>' + list()
    else:
        return f'City with ID {id} not found! <br>' + list()

@city_bp.route("/delete_city", methods=["POST", "GET"])
def delete():
    id = request.values.get("id")
    city = City.query.get(id)
    if city:
        db.session.delete(city)
        db.session.commit()
        return f'City {city.name} deleted successfully! <br>' + list()
    else:
        return f'City with ID {id} not found! <br>' + list()
    
@city_bp.route("/copy_city", methods=["POST", "GET"])
def copy():
    id = request.values.get("id")
    city = City.query.get(id)
    if city:
        new_city = City(name=city.name, latitude=city.latitude, longitude=city.longitude)
        db.session.add(new_city)
        db.session.commit()
        return f'City {city.name} copied successfully! <br>' + list()
    else:
        return f'City with ID {id} not found! <br>' + list()

