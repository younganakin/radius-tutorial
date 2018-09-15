from django.http import HttpResponse

import requests
import json


def index(request):
    push_url = 'http://pay.brandfi.co.ke:8301/api/stkpush'

    push_params = {
        "clientId": "2",
        "transactionType": "CustomerPayBillOnline",
        "phoneNumber": "254701854152",
        "amount": "1",
        "callbackUrl": "http://pay.brandfi.co.ke/payfi-success",
        "accountReference": "demo",
        "transactionDesc": "Test"
    }

    headers = {'Content-type': 'application/json'}

    r = requests.post(push_url, json=push_params, headers=headers)
    parsed_json = json.loads(r.text)
    print(parsed_json['MerchantRequestID'])
    print(parsed_json['CheckoutRequestID'])
    print(parsed_json['ResponseCode'])
    print(parsed_json['ResponseDescription'])
    print(parsed_json['CustomerMessage'])

    push_query_url = 'http://pay.brandfi.co.ke:8301/api/stkpushquery'

    push_query_params = {
        "clientId": "2",
        "checkoutRequestId": parsed_json['CheckoutRequestID']
    }

    print()

    return HttpResponse("Hello, world. You're at the mpesa index.")
