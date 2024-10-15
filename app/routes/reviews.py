from flask import Blueprint, request, jsonify
from app.models import Review, Hotel, User, db

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([{
        "id": review.id,
        "hotel": review.hotel.name,
        "user": review.user.username,
        "rating": review.rating,
        "comment": review.comment
    } for review in reviews])

@reviews_bp.route('/', methods=['POST'])
def create_review():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    hotel = Hotel.query.get(data['hotel_id'])
    if not user or not hotel:
        return jsonify({"message": "User or Hotel not found"}), 404
    new_review = Review(rating=data['rating'], comment=data['comment'], user=user, hotel=hotel)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review submitted successfully"}), 201
