from django.contrib import admin

# Register your models here.
from .models import *
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin


admin.site.register(Provider)
admin.site.register(ServiceArea)

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     readonly_fields = [
#         'date_joined', 'id'
#     ]