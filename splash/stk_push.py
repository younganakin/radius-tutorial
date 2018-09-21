from django.utils import timezone

import requests
import json
import re


class STKPushQuery(object):
    def __init__(self, checkoutRequestId, phone_number):
        self.checkoutRequestId = checkoutRequestId
        self.is_result = False
        self.result = None

    def push_query(self):
        headers = {'Content-type': 'application/json'}

        push_query_params = {
            "clientId": "2",
            "timestamp": timezone.now().strftime('%Y%m%d%H%M%S'),
            "checkoutRequestId": self.checkoutRequestId
        }

        push_query_url = 'http://pay.brandfi.co.ke:8301/api/stkpushquery'

        r = requests.post(
            push_query_url, json=push_query_params, headers=headers)

        response_json = json.loads(r.text)
        if self.check_error(response_json):
            result = response_json['errorMessage']
            if 'The transaction is being processed' == result:
                self.result = result
                self.is_result = False
        elif self.check_result(response_json):
            result = re.sub("[\(\[].*?[\)\]]", "", response_json['ResultDesc'])
            if 'Request cancelled by user' == result:
                self.result = result
                self.is_result = True
            elif 'Unable to lock subscriber, a transaction is already in process \
            for the current subscriber' == result:
                self.result = result
                self.is_result = True
            elif 'The balance is insufficient for the transaction' == result:
                self.result = result
                self.is_result = True
            elif 'The service request is processed successfully' == result:
                response_dict = [True, result]
                success_url = 'https://cubemobile.tech/dumprequest.txt'
                success_request = requests.get(success_url, verify=False)
                mobile_number = phone_number.replace("254", "0")
                # user_exists_url = 'http://radius.brandfi.co.ke/api/user/by-phone/' + mobile_number
                # r = requests.get(user_exists_url)
                registration_url = 'http://radius.brandfi.co.ke/api/registration'
                payload = {'uname': mobile_number,
                           'contact': mobile_number,
                           'status': '1'}

                r = requests.post(registration_url, params=payload)
                self.result = result
                self.is_result = True
            else:
                self.result = result
                self.is_result = True

    def check_error(self, response_json):
        try:
            error_message = response_json['errorMessage']
            return True
        except KeyError as error:
            return False

    def check_result(self, response_json):
        try:
            result = response_json['ResultDesc']
            return True
        except KeyError as error:
            return False
