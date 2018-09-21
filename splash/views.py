from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .stk_push import STKPushQuery
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from .models import Feedback
from django.utils import timezone

import requests
import json
import furl


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        login_url = request.session['login_url']
        success_url = 'http://' + request.get_host() + reverse('splash:home')

        request.session['artcafe_user'] = username
        login_params = {"username": username,
                        "password": password,
                        "success_url": success_url}

        r = requests.post(login_url, params=login_params)
        return HttpResponseRedirect(r.url)
    else:
        login_url = request.GET['login_url']
        continue_url = request.GET['continue_url']
        ap_name = request.GET['ap_name']
        ap_mac = request.GET['ap_mac']
        ap_tags = request.GET['ap_tags']
        client_ip = request.GET['client_ip']
        client_mac = request.GET['client_mac']

        # f = furl.furl(login_url)
        # f.remove(['continue_url'])
        request.session['login_url'] = login_url
        request.session['continue_url'] = continue_url
        request.session['ap_name'] = ap_name
        request.session['ap_mac'] = ap_mac
        request.session['ap_tags'] = ap_tags
        request.session['client_ip'] = client_ip
        request.session['client_mac'] = client_mac

    return render(request, 'splash/index.html')


def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        contact = request.POST['contact']

        registration_url = 'http://radius.brandfi.co.ke/api/registration'

        payload = {'uname': uname,
                   'fname': fname,
                   'lname': lname,
                   'email': email,
                   'contact': contact,
                   'status': '1'}

        r = requests.post(registration_url, params=payload)
        return HttpResponseRedirect(reverse('splash:register'))

    return render(request, 'splash/register.html')


def home(request):
    logout_url = request.GET['logout_url']
    continue_url = request.session['continue_url']
    context = {
        'logout_url': logout_url + '&' + continue_url,
    }
    return render(request, 'splash/home.html', context)


@api_view(['POST'])
def feedback(request):
    artcafe_user = request.session['artcafe_user']
    print(artcafe_user)

    service_rating = request.data['service']
    food_rating = request.data['food']
    atmosphere_rating = request.data['atmosphere']
    comment = request.data['comment']

    feedback = Feedback(service_rating=service_rating,
                        food_rating=food_rating,
                        atmosphere_rating=atmosphere_rating,
                        comment=comment,
                        username=artcafe_user,
                        logged_in=timezone.now())

    feedback.save()

    return JsonResponse({'message': 'Success'})


def payment(request):
    tarrifs_url = 'http://radius.brandfi.co.ke/api/tarrifs'

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['user_name']
        phone_number = request.POST['phone_number']
        tarrif_id = request.POST['policy']
        r = requests.get(tarrifs_url)
        tarrifs_json = json.loads(r.text)
        for tarrif in tarrifs_json:
            price = tarrif['price']

        stk_push(phone_number, price, first_name, last_name, user_name)
        return HttpResponseRedirect(everse('splash:home'))
    else:
        context = {
            'root_url': "",
        }

    return render(request, 'splash/pay-mpesa.html', context)


def stk_push(phone_number, price, first_name, last_name, user_name):
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
    mobile_number = phone_number.replace("254", "0")

    stk_push_query = STKPushQuery(
        checkoutRequestId, mobile_number, first_name, last_name, user_name)

    """Example of how to send server generated events to clients."""
    while not stk_push_query.is_result:
        stk_push_query.push_query()
        redis_publisher = RedisPublisher(facility='foobar', broadcast=True)
        message = RedisMessage(stk_push_query.result)
        redis_publisher.publish_message(message)

        if(stk_push_query.is_result):
            break
