from flask import Blueprint, request, jsonify
from app.models import Booking, Hotel, User, db
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([{
        "id": booking.id,
        "hotel": booking.hotel.name,
        "user": booking.user.username,
        "check_in": booking.check_in,
        "check_out": booking.check_out
    } for booking in bookings])

@bookings_bp.route('/', methods=['POST'])
def create_booking():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    hotel = Hotel.query.get(data['hotel_id'])
    if not user or not hotel:
        return jsonify({"message": "User or Hotel not found"}), 404
    new_booking = Booking(check_in=datetime.strptime(data['check_in'], '%Y-%m-%d'), check_out=datetime.strptime(data['check_out'], '%Y-%m-%d'), user=user, hotel=hotel)
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"message": "Booking created successfully"}), 201
