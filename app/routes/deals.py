from flask import Blueprint, request, jsonify
from app.models import Deal, db
from datetime import datetime

deals_bp = Blueprint('deals', __name__)

@deals_bp.route('/', methods=['GET'])
def get_deals():
    deals = Deal.query.filter(Deal.expiry_date > datetime.utcnow()).all()
    return jsonify([{
        "id": deal.id,
        "title": deal.title,
        "description": deal.description,
        "discount_percentage": deal.discount_percentage,
        "expiry_date": deal.expiry_date
    } for deal in deals])

@deals_bp.route('/', methods=['POST'])
def create_deal():
    data = request.get_json()
    new_deal = Deal(
        title=data['title'],
        description=data['description'],
        discount_percentage=data['discount_percentage'],
        expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d')
    )
    db.session.add(new_deal)
    db.session.commit()
    return jsonify({"message": "Deal created successfully"}), 201
