from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from djgeojson.fields import PointField
# Create your models here.

class Provider(models.Model):
  name = models.CharField(max_length=200)
  language = models.CharField(max_length=200)
  currency = models.CharField(max_length=200)
  phone_number = models.CharField(max_length=200)
  description = models.CharField(max_length=300)  
  created_date = models.DateTimeField(default=timezone.now)
  updated_date = models.DateTimeField(default=timezone.now)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name ="provider_creator")
  updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="provider_updator")

  def __str__(self):
    return str(self.id)


class ServiceArea(models.Model):
  provider = models.ForeignKey(Provider, on_delete=models.CASCADE,related_name ="provider")
  geom = PointField()
  name = models.CharField(max_length=200)
  price = models.CharField(max_length=200)
  description = models.CharField(max_length=300)  
  created_date = models.DateTimeField(default=timezone.now)
  updated_date = models.DateTimeField(default=timezone.now)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name ="service_creator")
  updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="service_updator")

  def __str__(self):
    return str(self.id)