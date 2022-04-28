from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from djgeojson.fields import PolygonField
# Create your models here.

class Provider(models.Model):
  name = models.CharField(max_length=200, null = True, blank = True)
  email = models.CharField(max_length=200,null = True, blank = True)
  language = models.CharField(max_length=200,null = True, blank = True)
  currency = models.CharField(max_length=200,null = True, blank = True)
  phone_number = models.CharField(max_length=200,null = True, blank = True)
  description = models.CharField(max_length=300,null = True, blank = True)  
  created_date = models.DateTimeField(default=timezone.now)
  updated_date = models.DateTimeField(default=timezone.now)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name ="provider_creator",default="1")
  updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="provider_updator",default="1")

  def __str__(self):
    return str(self.id)


class ServiceArea(models.Model):
  provider = models.ForeignKey(Provider, on_delete=models.CASCADE,related_name ="provider")
  geom = PolygonField()
  name = models.CharField(max_length=200,null = True, blank = True)
  price = models.CharField(max_length=200,null = True, blank = True)
  description = models.CharField(max_length=300,null = True, blank = True)  
  created_date = models.DateTimeField(default=timezone.now)
  updated_date = models.DateTimeField(default=timezone.now)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name ="service_creator",default="1")
  updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="service_updator",default="1")

  def __str__(self):
    return str(self.id)