from django.db import models

# Create your models here.


class Feedback(models.Model):
    service_rating = models.CharField(max_length=200)
    food_rating = models.CharField(max_length=200)
    atmosphere_rating = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    logged_in = models.DateTimeField()
