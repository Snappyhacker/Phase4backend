from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    amenities = db.Column(db.String(250), nullable=False)

    # Relationship using back_populates
    rooms = db.relationship('Room', back_populates='hotel', lazy=True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    features = db.Column(db.String(500), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)  # Adding rating to Room model

    # Relationship using back_populates
    hotel = db.relationship('Hotel', back_populates='rooms', lazy=True)

    def __init__(self, hotel_id, room_type, features, price_per_night, rating):
        self.hotel_id = hotel_id
        self.room_type = room_type
        self.features = features
        self.price_per_night = price_per_night
        self.rating = rating

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # New column to track payment status
    payment_status = db.Column(db.String(20), nullable=True, default="Pending")  # Default to 'Pending'

    def __init__(self, user_id, room_id, check_in_date, check_out_date, total_price, payment_status="Pending"):
        self.user_id = user_id
        self.room_id = room_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_price = total_price
        self.payment_status = payment_status


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)

# New Payment Model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # e.g., 'Mpesa', 'Bank Card'
    transaction_status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    payment_trigger_payload = db.Column(db.JSON, default=None, nullable=True)
    payment_trigger_response = db.Column(db.JSON, default=None, nullable=True)
    payment_processing_response =  db.Column(db.JSON, default=None, nullable=True)
    checkout_request_id = db.Column(db.String(50), nullable=True)
    merchant_request_id = db.Column(db.String(50), nullable=True)