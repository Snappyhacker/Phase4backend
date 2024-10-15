import os
from datetime import date  # Import date to create date objects
from app import create_app, db
from app.models import User, Hotel, Booking, Review, Deal

# Create the Flask app
app = create_app()

# Sample data
users_data = [
    {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1'},
    {'username': 'user2', 'email': 'user2@example.com', 'password': 'password2'},
    {'username': 'user3', 'email': 'user3@example.com', 'password': 'password3'},
]

hotels_data = [
    {'name': 'Hotel Paradise', 'location': 'Nairobi', 'price': 100, 'rating': 4.5, 'amenities': 'Free WiFi, Pool'},
    {'name': 'Cozy Inn', 'location': 'Mombasa', 'price': 80, 'rating': 4.0, 'amenities': 'Breakfast Included'},
    {'name': 'Luxury Suites', 'location': 'Nairobi', 'price': 200, 'rating': 5.0, 'amenities': 'Spa, Gym, Free Parking'},
]

bookings_data = [
    {'user_id': 1, 'hotel_id': 1, 'check_in_date': date(2024, 10, 20), 'check_out_date': date(2024, 10, 25), 'total_price': 500},
    {'user_id': 2, 'hotel_id': 2, 'check_in_date': date(2024, 11, 1), 'check_out_date': date(2024, 11, 5), 'total_price': 320},
]

reviews_data = [
    {'user_id': 1, 'hotel_id': 1, 'rating': 5, 'comment': 'Amazing experience!'},
    {'user_id': 2, 'hotel_id': 2, 'rating': 4, 'comment': 'Nice stay, would come again.'},
]

deals_data = [
    {'hotel_id': 1, 'description': '20% off for weekends!', 'expiration_date': date(2024, 12, 31)},
    {'hotel_id': 2, 'description': 'Free breakfast for all bookings!', 'expiration_date': date(2024, 11, 30)},
]

# Function to seed data
def seed_data():
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        # Seed Users
        for user in users_data:
            new_user = User(username=user['username'], email=user['email'])
            new_user.set_password(user['password'])  # Make sure to use your hashing function
            db.session.add(new_user)

        # Seed Hotels
        for hotel in hotels_data:
            new_hotel = Hotel(name=hotel['name'], location=hotel['location'], price=hotel['price'], 
                              rating=hotel['rating'], amenities=hotel['amenities'])
            db.session.add(new_hotel)

        # Seed Bookings
        for booking in bookings_data:
            new_booking = Booking(
                user_id=booking['user_id'], 
                hotel_id=booking['hotel_id'],
                check_in_date=booking['check_in_date'], 
                check_out_date=booking['check_out_date'],
                total_price=booking['total_price']
            )
            db.session.add(new_booking)

        # Seed Reviews
        for review in reviews_data:
            new_review = Review(
                user_id=review['user_id'], 
                hotel_id=review['hotel_id'],
                rating=review['rating'], 
                comment=review['comment']
            )
            db.session.add(new_review)

        # Seed Deals
        for deal in deals_data:
            new_deal = Deal(
                hotel_id=deal['hotel_id'], 
                description=deal['description'],
                expiration_date=deal['expiration_date']
            )
            db.session.add(new_deal)

        db.session.commit()  # Commit all changes to the database
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
