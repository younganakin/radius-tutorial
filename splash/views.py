from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import requests


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        username = request.POST['username']
        code = request.POST['code']

        login_url = request.session['login_url']
        continue_url = request.session['continue_url']

        login_params = {"username": username,
                        "password": code,
                        "continue_url": "https://www.google.com/"}

        headers = {'Content-type': 'application/json'}

        r = requests.post(login_url, json=login_params, headers=headers)
        print(r.status_code)
        # return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    else:
        login_url = request.GET['login_url']
        continue_url = request.GET['continue_url']
        ap_name = request.GET['ap_name']
        ap_mac = request.GET['ap_mac']
        ap_tags = request.GET['ap_tags']
        client_ip = request.GET['client_ip']
        client_mac = request.GET['client_mac']

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
        print(r.status_code)
        return HttpResponseRedirect(reverse('splash:index'))

    return render(request, 'splash/register.html')


@api_view(['POST'])
def register_api(request):
    registration_url = 'http://radius.brandfi.co.ke/api/registration'

    uname = request.data['uname']
    fname = request.data['fname']
    lname = request.data['lname']
    email = request.data['email']
    contact = request.data['contact']

    payload = {'uname': uname,
               'fname': fname,
               'lname': lname,
               'email': email,
               'contact': contact,
               'status': '1'}

    r = requests.post(registration_url, params=payload)
    # return HttpResponseRedirect(reverse('splash:index'))
    return Response(r.content)
