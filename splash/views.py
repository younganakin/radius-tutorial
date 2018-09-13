from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import requests


def index(request):
    return render(request, 'splash/index.html')


def register(request):
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
    return Response(r.content)
