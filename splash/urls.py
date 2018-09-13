from django.urls import path

from . import views

app_name = 'splash'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    # ex: /splash/api/register/
    path('api/register/',
         views.register_api,
         name='register_api'),
]
