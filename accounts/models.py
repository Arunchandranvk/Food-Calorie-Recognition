from django.db import models
from django.contrib.auth.models import AbstractUser
# from rest_framework import serializers
# Create your models here.


class CustUser(AbstractUser):
    phone=models.IntegerField(null=True)


class FoodImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    predicted_food = models.CharField(max_length=100)
    calories_data = models.JSONField()
    predicted_volume = models.CharField(max_length=100)

