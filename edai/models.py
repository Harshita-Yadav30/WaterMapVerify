from django.db import models
from django.contrib.auth.models import User
import datetime

class Location(models.Model):
    date_diff = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date(2024, 5, 15))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='uploads/', default=0)
    video = models.FileField(upload_to='uploads/')
    place = models.CharField(max_length=100)
    description = models.TextField()
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
