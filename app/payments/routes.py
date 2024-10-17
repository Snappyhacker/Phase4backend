from flask import Blueprint, request, jsonify
import requests
from app.models import Payment
from app import db

payments_bp = Blueprint("payments", __name__)

# You share this i will find you
PAYSTACK_SECRET_KEY = "sk_live_ae8eed68829a37618a7dc3af22e6be9ba1fc713f"
PAYSTACK_API_URL = "https://api.paystack.co"


class TransactionStatus:
    PENDING = "PENDING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


@payments_bp.route("/paystack/initialize", methods=["POST"])
def initialize_paystack_payment():
    data = request.get_json()

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "email": data.get("email"),
        "amount": int(
            float(data.get("amount")) * 100
        ),  # Paystack expects amount in kobo
        "callback_url": data.get("callback_url"),
    }

    response = requests.post(
        f"{PAYSTACK_API_URL}/transaction/initialize", json=payload, headers=headers
    )
    transaction_data = response.json()
    print(transaction_data)

    if transaction_data.get("status"):
        new_payment = Payment(
            amount=float(data.get("amount")),
            payment_method="paystack",
            transaction_status=TransactionStatus.PENDING,
            payment_trigger_payload=data,
            payment_trigger_response=transaction_data,
            checkout_request_id=transaction_data["data"]["reference"],
            merchant_request_id=transaction_data["data"]["access_code"],
        )
        new_payment.booking_id = data.get("booking_id")

        db.session.add(new_payment)
        db.session.commit()

        return jsonify(
            {
                "reference": transaction_data["data"]["reference"],
                "authorization_url": transaction_data["data"]["authorization_url"],
            }
        ), 200
    else:
        return jsonify({"error": "Failed to initialize transaction"}), 400


@payments_bp.route("/paystack/verify/<reference>", methods=["GET"])
def verify_payment(reference):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(
        f"{PAYSTACK_API_URL}/transaction/verify/{reference}", headers=headers
    )
    verification_data = response.json()

    payment = db.session.execute(
        db.select(Payment).filter_by(checkout_request_id=reference)
    ).scalar_one_or_none()

    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    payment.payment_processing_response = verification_data

    if (
        verification_data.get("status")
        and verification_data["data"]["status"] == "success"
    ):
        payment.transaction_status = TransactionStatus.COMPLETED
        db.session.commit()
        return jsonify(
            {"status": "success", "message": "Payment verified successfully"}
        ), 200
    else:
        payment.transaction_status = TransactionStatus.FAILED
        db.session.commit()
        return jsonify(
            {"status": "failed", "message": "Payment verification failed"}
        ), 400


@payments_bp.route("/paystack/webhook", methods=["POST"])
def paystack_webhook():
    payload = request.get_json()

    if payload.get("event") == "charge.success":
        reference = payload["data"]["reference"]
        payment = db.session.execute(
            db.select(Payment).filter_by(checkout_request_id=reference)
        ).scalar_one_or_none()

        if payment:
            payment.payment_processing_response = payload
            payment.transaction_status = TransactionStatus.COMPLETED
            db.session.commit()

    return jsonify({"status": "success"}), 200
