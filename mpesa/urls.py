from django.urls import path

from . import views

app_name = 'mpesa'

urlpatterns = [
    path('', views.index, name='index'),
]
