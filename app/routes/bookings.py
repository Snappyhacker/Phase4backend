from flask import Blueprint, request, jsonify
from app.models import Booking, db, Hotel, User
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/create', methods=['POST'])
def create_booking():
    data = request.get_json()

    user_id = data.get('user_id')
    hotel_id = data.get('hotel_id')
    check_in_date = data.get('check_in_date')
    check_out_date = data.get('check_out_date')
    total_price = data.get('total_price')

    # Validate if hotel and user exist
    user = User.query.get(user_id)
    hotel = Hotel.query.get(hotel_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404
    if not hotel:
        return jsonify({'message': 'Hotel not found'}), 404

    # Convert dates from string to datetime objects
    try:
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400

    new_booking = Booking(
        user_id=user_id,
        hotel_id=hotel_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        total_price=total_price
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message': 'Booking created successfully!', 'booking_id': new_booking.id}), 201
