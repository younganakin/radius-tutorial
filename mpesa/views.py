from django.http import HttpResponseRedirect
from .background import RepeatedTimer
from time import sleep
from django.shortcuts import render
from .tasks import push_query

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
        root_url = 'http://' + request.get_host() + request.get_full_path()

        f = furl.furl(login_url)
        f.remove(['continue_url'])
        request.session['login_url'] = f.url
        request.session['continue_url'] = continue_url
        request.session['ap_name'] = ap_name
        request.session['ap_mac'] = ap_mac
        request.session['ap_tags'] = ap_tags
        request.session['client_ip'] = client_ip
        request.session['client_mac'] = client_mac
        request.session['root_url'] = root_url

    return render(request, 'mpesa/index.html')


def pay_mpesa(request):
    root_url = request.session['root_url']

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        stk_push(phone_number)
        return HttpResponseRedirect(root_url)
    else:
        context = {
            'root_url': root_url,
        }

    return render(request, 'mpesa/pay-mpesa.html', context)


def stk_push(phone_number):
    push_url = 'http://pay.brandfi.co.ke:8301/api/stkpush'

    push_params = {
        "clientId": "2",
        "transactionType": "CustomerPayBillOnline",
        "phoneNumber": phone_number,
        "amount": "1",
        "callbackUrl": "http://pay.brandfi.co.ke/payfi-success",
        "accountReference": "demo",
        "transactionDesc": "Test"
    }

    headers = {'Content-type': 'application/json'}

    r = requests.post(push_url, json=push_params, headers=headers)
    parsed_json = json.loads(r.text)

    checkoutRequestId = parsed_json['CheckoutRequestID']
    result = push_query.delay(checkoutRequestId)

    if result:
        result.revoke()

    print("end of task")
