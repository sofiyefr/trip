from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.destination import Destination
from app.models.user import User

destinations_bp = Blueprint('destinations', __name__)

@destinations_bp.route('/', methods=['GET'])
def get_destinations():
    # Get query parameters for filtering
    country = request.args.get('country')
    city = request.args.get('city')
    
    query = Destination.query
    
    if country:
        query = query.filter(Destination.country.ilike(f'%{country}%'))
    if city:
        query = query.filter(Destination.city.ilike(f'%{city}%'))
    
    destinations = query.all()
    return jsonify([dest.to_dict() for dest in destinations]), 200

@destinations_bp.route('/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404
    
    return jsonify(destination.to_dict()), 200

@destinations_bp.route('/', methods=['POST'])
@jwt_required()
def create_destination():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    destination = Destination(
        name=data['name'],
        country=data['country'],
        city=data.get('city'),
        description=data.get('description'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    
    db.session.add(destination)
    db.session.commit()
    
    return jsonify(destination.to_dict()), 201

@destinations_bp.route('/<int:destination_id>', methods=['PUT'])
@jwt_required()
def update_destination(destination_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    destination = Destination.query.get(destination_id)
    
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        destination.name = data['name']
    if 'country' in data:
        destination.country = data['country']
    if 'city' in data:
        destination.city = data['city']
    if 'description' in data:
        destination.description = data['description']
    if 'latitude' in data:
        destination.latitude = data['latitude']
    if 'longitude' in data:
        destination.longitude = data['longitude']
    
    db.session.commit()
    return jsonify(destination.to_dict()), 200

@destinations_bp.route('/<int:destination_id>', methods=['DELETE'])
@jwt_required()
def delete_destination(destination_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    destination = Destination.query.get(destination_id)
    
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404
    
    db.session.delete(destination)
    db.session.commit()
    
    return jsonify({'message': 'Destination deleted successfully'}), 200 