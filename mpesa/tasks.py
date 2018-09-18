from celery import shared_task
from django.utils import timezone

import requests
import json
import re


@shared_task
def push_query(checkoutRequestId):
    headers = {'Content-type': 'application/json'}

    push_query_params = {
        "clientId": "2",
        "timestamp": timezone.now().strftime('%Y%m%d%H%M%S'),
        "checkoutRequestId": checkoutRequestId
    }

    push_query_url = 'http://pay.brandfi.co.ke:8301/api/stkpushquery'

    r = requests.post(push_query_url, json=push_query_params, headers=headers)

    response_json = json.loads(r.text)
    if check_error(response_json):
        result = response_json['errorMessage']
        if 'The transaction is being processed' == result:
            response_dict = [False, result]
            print(result)
            return False
    elif check_result(response_json):
        result = re.sub("[\(\[].*?[\)\]]", "", response_json['ResultDesc'])
        if 'Request cancelled by user' == result:
            response_dict = [True, result]
            print(result)
            return True
        elif 'Unable to lock subscriber, a transaction is already in process \
        for the current subscriber' == result:
            response_dict = [True, result]
            return True
        elif 'The balance is insufficient for the transaction' == result:
            response_dict = [True, result]
            return True
        elif 'The service request is processed successfully' == result:
            response_dict = [True, result]
            success_url = 'https://cubemobile.tech/dumprequest.txt'
            success_request = requests.get(success_url, verify=False)
            print(success_request.text)
            return True
        else:
            response_dict = [True, result]
            return True


def check_error(response_json):
    try:
        error_message = response_json['errorMessage']
        return True
    except KeyError as error:
        return False


def check_result(response_json):
    try:
        result = response_json['ResultDesc']
        return True
    except KeyError as error:
        return False
