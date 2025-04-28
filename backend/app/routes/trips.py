from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.trip import Trip
from app.models.route_point import RoutePoint
from datetime import datetime

trips_bp = Blueprint('trips', __name__)

def safe_int_conversion(value):
    """Safely convert a value to integer, returning None if conversion fails."""
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None

@trips_bp.route('/', methods=['GET', 'OPTIONS'])
def get_trips():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    # Apply JWT protection
    @jwt_required()
    def protected_get():
        try:
            user_id = get_jwt_identity()
            # Convert user_id to integer
            user_id_int = safe_int_conversion(user_id)
            
            if user_id_int is None:
                return jsonify({
                    'error': 'Invalid user ID format',
                    'message': 'Could not process the user identification'
                }), 400
                
            trips = Trip.query.filter_by(user_id=user_id_int).all()
            return jsonify({
                'trips': [trip.to_dict() for trip in trips]
            }), 200
        except Exception as e:
            print(f"Error in get_trips: {str(e)}")
            return jsonify({
                'error': 'Failed to fetch trips',
                'message': str(e)
            }), 400
    
    try:
        return protected_get()
    except Exception as e:
        print(f"JWT Error: {str(e)}")
        return jsonify({
            'error': 'Authentication error',
            'message': str(e)
        }), 401

@trips_bp.route('/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_trip(trip_id):
    try:
        user_id = get_jwt_identity()
        user_id_int = safe_int_conversion(user_id)
        
        if user_id_int is None:
            return jsonify({
                'error': 'Invalid user ID format',
                'message': 'Could not process the user identification'
            }), 400
        
        trip = Trip.query.filter_by(id=trip_id, user_id=user_id_int).first()
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        return jsonify(trip.to_dict()), 200
    except Exception as e:
        print(f"Error in get_trip: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch trip',
            'message': str(e)
        }), 400

@trips_bp.route('/', methods=['POST'])
@jwt_required()
def create_trip():
    try:
        user_id = get_jwt_identity()
        user_id_int = safe_int_conversion(user_id)
        
        if user_id_int is None:
            return jsonify({
                'error': 'Invalid user ID format',
                'message': 'Could not process the user identification'
            }), 400
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'No JSON data provided'
            }), 400
        
        required_fields = ['title', 'start_date', 'end_date', 'route_points']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'message': f'The following fields are required: {", ".join(missing_fields)}'
            }), 400
        
        # Validate route points
        route_points = data.get('route_points', [])
        if not route_points or len(route_points) < 2:
            return jsonify({
                'error': 'Invalid route',
                'message': 'At least two route points are required'
            }), 400

        trip = Trip(
            title=data['title'],
            description=data.get('description'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            budget=data.get('budget', 0.0),
            is_public=data.get('is_public', False),
            user_id=user_id_int
        )
        
        # Add route points
        for i, point in enumerate(route_points):
            route_point = RoutePoint(
                city=point['city'],
                transportation_type=point.get('transportation_type'),
                order_number=i
            )
            trip.route_points.append(route_point)
        
        db.session.add(trip)
        db.session.commit()
        
        return jsonify(trip.to_dict()), 201
    except ValueError as e:
        print(f"Validation error in create_trip: {str(e)}")
        return jsonify({
            'error': 'Invalid data format',
            'message': str(e)
        }), 400
    except Exception as e:
        print(f"Error in create_trip: {str(e)}")
        return jsonify({
            'error': 'Failed to create trip',
            'message': str(e)
        }), 400

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    try:
        user_id = get_jwt_identity()
        user_id_int = safe_int_conversion(user_id)
        
        if user_id_int is None:
            return jsonify({
                'error': 'Invalid user ID format',
                'message': 'Could not process the user identification'
            }), 400
        
        trip = Trip.query.filter_by(id=trip_id, user_id=user_id_int).first()
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'No JSON data provided'
            }), 400
        
        # Update basic trip information
        if 'title' in data:
            trip.title = data['title']
        if 'description' in data:
            trip.description = data['description']
        if 'start_date' in data:
            trip.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data:
            trip.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        if 'budget' in data:
            trip.budget = data['budget']
        if 'is_public' in data:
            trip.is_public = data['is_public']
            
        # Update route points
        if 'route_points' in data:
            # Delete existing route points
            RoutePoint.query.filter_by(trip_id=trip.id).delete()
            
            # Add new route points
            for point_data in data['route_points']:
                route_point = RoutePoint(
                    trip_id=trip.id,
                    city=point_data['city'],
                    transportation_type=point_data.get('transportation_type'),
                    order_number=point_data.get('order_number', 0)
                )
                db.session.add(route_point)
        
        db.session.commit()
        return jsonify(trip.to_dict()), 200
    except ValueError as e:
        print(f"Validation error in update_trip: {str(e)}")
        return jsonify({
            'error': 'Invalid data format',
            'message': str(e)
        }), 400
    except Exception as e:
        print(f"Error in update_trip: {str(e)}")
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update trip',
            'message': str(e)
        }), 400

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trip(trip_id):
    try:
        user_id = get_jwt_identity()
        user_id_int = safe_int_conversion(user_id)
        
        if user_id_int is None:
            return jsonify({
                'error': 'Invalid user ID format',
                'message': 'Could not process the user identification'
            }), 400
        
        trip = Trip.query.filter_by(id=trip_id, user_id=user_id_int).first()
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        db.session.delete(trip)
        db.session.commit()
        
        return jsonify({'message': 'Trip deleted successfully'}), 200
    except Exception as e:
        print(f"Error in delete_trip: {str(e)}")
        return jsonify({
            'error': 'Failed to delete trip',
            'message': str(e)
        }), 400 