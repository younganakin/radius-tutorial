from django.urls import path

from . import views

app_name = 'splash'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('api/feedback/', views.feedback, name='feedback'),
    path('payment/', views.payment, name='payment'),
]
