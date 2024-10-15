from flask import Blueprint, request, jsonify
from app.models import Hotel, db

hotels_bp = Blueprint('hotels', __name__)

@hotels_bp.route('/', methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()
    return jsonify([{"id": hotel.id, "name": hotel.name, "location": hotel.location} for hotel in hotels])

@hotels_bp.route('/', methods=['POST'])
def create_hotel():
    data = request.get_json()
    new_hotel = Hotel(name=data['name'], location=data['location'], price_per_night=data['price_per_night'], rooms_available=data['rooms_available'])
    db.session.add(new_hotel)
    db.session.commit()
    return jsonify({"message": "Hotel created successfully"}), 201

@hotels_bp.route('/<int:id>', methods=['PUT'])
def update_hotel(id):
    data = request.get_json()
    hotel = Hotel.query.get_or_404(id)
    hotel.name = data['name']
    hotel.location = data['location']
    hotel.price_per_night = data['price_per_night']
    hotel.rooms_available = data['rooms_available']
    db.session.commit()
    return jsonify({"message": "Hotel updated successfully"}), 200

@hotels_bp.route('/<int:id>', methods=['DELETE'])
def delete_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    db.session.delete(hotel)
    db.session.commit()
    return jsonify({"message": "Hotel deleted successfully"}), 200
