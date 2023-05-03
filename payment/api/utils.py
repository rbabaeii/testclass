import requests
from django.conf import settings


    #? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


def get_payment_gateway(amount, description, user_phone):
    ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
    merchant_id = '1344b5d4-0048-11e8-94db-005056a205be'
    data = {
        'Amount': amount, 
        'MerchantID': merchant_id, 
        'Description': 'test',
        'Mobile': user_phone,
        'CallbackURL': 'http://localhost:8000/api/v1/payments/pay/verify/'
    }
    r = requests.post(ZP_API_REQUEST, json=data)
    return r.json()



def verify_payment(authority, amount):
    ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
    merchant_id = '1344b5d4-0048-11e8-94db-005056a205be'
    data = {
        'MerchantID': merchant_id,
        'Authority': authority,
        'Amount': amount,
    }
    r = requests.post(ZP_API_VERIFY, json=data)
    return r.json()