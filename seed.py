import os
from datetime import date
from app import create_app, db
from app.models import User, Room, Booking, Review, Deal, Hotel

# Create the Flask app
app = create_app()

# Sample data
users_data = [
    {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1'},
    {'username': 'user2', 'email': 'user2@example.com', 'password': 'password2'},
    {'username': 'user3', 'email': 'user3@example.com', 'password': 'password3'},
]

# Define a single hotel without rating
hotel_data = {
    'name': 'Swifty Hotel',
    'location': 'Beachfront',
    'amenities': 'Pool, Spa, Free Breakfast'
}

# Room details with features and ratings
rooms_data = [
    {
        'room_type': 'Single Room',
        'price': 1,  # Price per night
        'rating': 4.5,
        'amenities': 'Cozy and comfortable, designed for solo travelers, free WiFi, mini bar, affordable rate, work desk available, access to hotel facilities.'
    },
    {
        'room_type': 'Double Room',
        'price': 1,  # Price per night
        'rating': 4.0,
        'amenities': 'Spacious interiors, modern decor, free WiFi, mini fridge, two queen-sized beds, ideal for families or friends, access to pool and gym.'
    },
    {
        'room_type': 'Deluxe Room',
        'price': 2,  # Price per night
        'rating': 5.0,
        'amenities': 'Breath-taking ocean views, private balcony, free WiFi, air conditioning, room service available, king-sized bed, complimentary breakfast.'
    },
    {
        'room_type': 'Luxury Suite',
        'price': 2,  # Price per night
        'rating': 5.0,
        'amenities': 'Premium furnishings, top-notch amenities, private jacuzzi, free WiFi, exceptional room service, oceanfront view, complimentary spa access.'
    },
]

bookings_data = [
    {'user_id': 1, 'room_id': 1, 'check_in_date': date(2024, 10, 20), 'check_out_date': date(2024, 10, 25), 'total_price': 2},  # Updated total price
    {'user_id': 2, 'room_id': 2, 'check_in_date': date(2024, 11, 1), 'check_out_date': date(2024, 11, 5), 'total_price': 2},  # Updated total price
]

reviews_data = [
    {'user_id': 1, 'room_id': 1, 'rating': 5, 'comment': 'Amazing experience!'},
    {'user_id': 2, 'room_id': 2, 'rating': 4, 'comment': 'Nice stay, would come again.'},
]

deals_data = [
    {'room_id': 1, 'description': '20% off for weekends!', 'expiration_date': date(2024, 12, 31)},
    {'room_id': 2, 'description': 'Free breakfast for all bookings!', 'expiration_date': date(2024, 11, 30)},
]

# Function to seed data
def seed_data():
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        # Seed the single hotel
        new_hotel = Hotel(
            name=hotel_data['name'], 
            location=hotel_data['location'], 
            amenities=hotel_data['amenities']
        )
        db.session.add(new_hotel)
        db.session.commit()  # Commit to get hotel ID

        # Seed Users
        for user in users_data:
            new_user = User(username=user['username'], email=user['email'])
            new_user.set_password(user['password'])  
            db.session.add(new_user)

        # Seed Rooms
        for room in rooms_data:
            new_room = Room(
                room_type=room['room_type'], 
                hotel_id=new_hotel.id,  # Reference to the one existing hotel
                price_per_night=room['price'], 
                rating=room['rating'], 
                features=room['amenities']  # Correct field name for amenities
            )
            db.session.add(new_room)

        # Seed Bookings
        for booking in bookings_data:
            new_booking = Booking(
                user_id=booking['user_id'], 
                room_id=booking['room_id'],  # Reference to the room
                check_in_date=booking['check_in_date'], 
                check_out_date=booking['check_out_date'],
                total_price=booking['total_price']
            )
            db.session.add(new_booking)

        # Seed Reviews
        for review in reviews_data:
            new_review = Review(
                user_id=review['user_id'], 
                room_id=review['room_id'],  # Reference to the room
                rating=review['rating'], 
                comment=review['comment']
            )
            db.session.add(new_review)

        # Seed Deals
        for deal in deals_data:
            new_deal = Deal(
                room_id=deal['room_id'],  # Reference to the room
                description=deal['description'],
                expiration_date=deal['expiration_date']
            )
            db.session.add(new_deal)

        db.session.commit()  # Commit all changes to the database
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
