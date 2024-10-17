import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
import base64


DARAJA_CONSUMER_KEY = 'qPnG6LXwJlhqKiXnDwhA64zpVPrX7sXe731yKbtx7IZu3WuQ'
DARAJA_CONSUMER_SECRET = 'hV5gUJoGaIlLfGOoAjeHpt5LjakWhYMDglIopLWzMIjOOWNQxPV8dep5VvirivDL'
DARAJA_AUTH_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
DARAJA_ONLINE_PASS_KEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
DARAJA_LIPA_NA_MPESA_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
# DARAJA_LIPA_NA_MPESA_CALLBACK_URL = 'https://sandbox.safaricom.co.ke/mpesa/'
DARAJA_LIPA_NA_MPESA_CALLBACK_URL='https://e21d-91-102-180-58.ngrok-free.app/payments/mpesa/process'
BUSINESS_SHORT_CODE = '174379'


class Credentials:
  consumer_key = DARAJA_CONSUMER_KEY
  consumer_secret = DARAJA_CONSUMER_SECRET
  api_URL = DARAJA_AUTH_URL
  online_pass_key = DARAJA_ONLINE_PASS_KEY


class AccessToken:
  @classmethod
  def get_access_token(cls):
    response = requests.get(
        url=Credentials.api_URL,
        auth=HTTPBasicAuth(
            username=Credentials.consumer_key,
            password=Credentials.consumer_secret
        )
    )

    token = json.loads(response.text).get('access_token')

    return response, token


class LipaNaMpesaPassword:
  payment_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

  def __init__(self, short_code):
    self.business_short_code = str(short_code)
    self.data_to_encode = self.business_short_code + \
        Credentials.online_pass_key + self.payment_time
    self.online_password = base64.b64encode(self.data_to_encode.encode())
    self.decoded_password = self.online_password.decode('utf-8')


class Mpesa(LipaNaMpesaPassword):
  LIPA_NA_MPESA_URL = DARAJA_LIPA_NA_MPESA_URL
  LIPA_NA_MPESA_CALLBACK_URL = DARAJA_LIPA_NA_MPESA_CALLBACK_URL

  def __init__(self, short_code = BUSINESS_SHORT_CODE):
    super().__init__(short_code=short_code)

  def make_payment(self, payer_number, amount, description, reference):
    token_response, access_token = AccessToken.get_access_token()

    payment_request_body = {
        'InitiatorName': Credentials.consumer_key,
        'BusinessShortCode': self.business_short_code,
        'Password': self.decoded_password,
        'Timestamp': self.payment_time,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': payer_number,
        'PartyB': self.business_short_code,
        'PhoneNumber': payer_number,
        'CallBackURL': self.LIPA_NA_MPESA_CALLBACK_URL,
        'AccountReference': reference,
        'TransactionDesc': description
    }

    response = requests.post(
        url=self.LIPA_NA_MPESA_URL,
        json=payment_request_body,
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        }
    )

    return response, json.loads(response.text)