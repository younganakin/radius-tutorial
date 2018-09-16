from django.http import HttpResponse
from django.utils import timezone
from .background import RepeatedTimer
from time import sleep
from django.shortcuts import render

import requests
import json
import re
import furl


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        username = request.POST['username']
        code = request.POST['code']

        login_url = request.session['login_url']
        continue_url = 'http://' + request.get_host() + reverse('splash:home')

        login_params = {"username": username,
                        "password": code,
                        "continue_url": continue_url}

        # headers = {'Content-type': 'application/json'}

        r = requests.post(login_url, params=login_params)
        print(r.url)
        # return HttpResponseRedirect(reverse('splash:home'))
    # if a GET (or any other method) we'll create a blank form
    else:
        login_url = request.GET['login_url']
        continue_url = request.GET['continue_url']
        ap_name = request.GET['ap_name']
        ap_mac = request.GET['ap_mac']
        ap_tags = request.GET['ap_tags']
        client_ip = request.GET['client_ip']
        client_mac = request.GET['client_mac']

        f = furl.furl(login_url)
        f.remove(['continue_url'])
        request.session['login_url'] = f.url
        request.session['continue_url'] = continue_url
        request.session['ap_name'] = ap_name
        request.session['ap_mac'] = ap_mac
        request.session['ap_tags'] = ap_tags
        request.session['client_ip'] = client_ip
        request.session['client_mac'] = client_mac

    return render(request, 'mpesa/index.html')


def pay_mpesa(request):
    return render(request, 'mpesa/pay-mpesa.html')


def stk_push(request):
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

    checkoutRequestId = parsed_json['CheckoutRequestID']
    # it auto-starts, no need of rt.start()
    rt = RepeatedTimer(1, print_json, checkoutRequestId)
    try:
        sleep(40)
    finally:
        rt.stop()

    print("end of timer")

    return HttpResponse("Hello, world. You're at the mpesa index.")


def print_json(checkoutRequestId):
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
            return response_dict
    elif check_result(response_json):
        result = re.sub("[\(\[].*?[\)\]]", "", response_json['ResultDesc'])
        if 'Request cancelled by user' == result:
            response_dict = [True, result]
            return response_dict
        elif 'Unable to lock subscriber, a transaction is already in process \
        for the current subscriber' == result:
            response_dict = [True, result]
            return response_dict
        elif 'The balance is insufficient for the transaction' == result:
            response_dict = [True, result]
            return response_dict
        elif 'The service request is processed successfully' == result:
            response_dict = [True, result]
            success_url = 'https://cubemobile.tech/dumprequest.txt'
            success_request = requests.get(success_url, verify=False)
            print(success_request.text)
            return response_dict
        else:
            response_dict = [True, result]
            return response_dict


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
