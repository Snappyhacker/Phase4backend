from flask import Blueprint, request, jsonify
from app.payments.mpesa.mpesa import Mpesa
from app.models import Payment
from app import db

payments_bp = Blueprint('payments', __name__)

class TransactionStatus:
    NEW = "NEW"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"

@payments_bp.route('/mpesa/pay', methods=['POST'])
def make_mpesa_payment():
    data = request.get_json()
    mpesa = Mpesa()
    
    booking_id = data.get('reference')
    amount = data.get('amount')

    response, transaction_data = mpesa.make_payment(
        payer_number=data.get('payer_number'),
        amount=amount,
        description=data.get('description'),
        reference=booking_id
    )
    is_successful = transaction_data.get('ResultCode') == 0

    new_payment = Payment(
        booking_id = booking_id,
        amount = float(amount),
        payment_method="mpesa",
        transaction_status=TransactionStatus.NEW if is_successful else TransactionStatus.FAILED,
        payment_trigger_payload = data,
        payment_trigger_response = transaction_data,
        checkout_request_id=transaction_data.get('CheckoutRequestID'),
        merchant_request_id=transaction_data.get('MerchantRequestID')
    )
    db.session.add(new_payment)
    db.session.commit()

    return jsonify(transaction_data), response.status_code

@payments_bp.route('/mpesa/process', methods=['POST'])
def process_payment():
    data = request.get_json()
    checkout_request_id = data.get('Body').get('stkCallback').get('CheckoutRequestID')
    is_successful = data.get('Body').get('stkCallback').get('ResultCode') == 0
    payment = db.session.execute(db.select(Payment).filter_by(checkout_request_id=checkout_request_id)).scalar_one()
    payment.payment_processing_response = data
    payment.transaction_status = TransactionStatus.COMPLETED if is_successful else TransactionStatus.FAILED
    db.session.commit()
    return jsonify(data), 200
