"""mozio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from provider.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('serviceArea', ServiceAreaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    # provider apis url
    path('getprovider', get_provider),
    path('getproviderwithpages',get_provider_with_page.as_view({'get': 'list'})),
    path('addprovider', add_providers),
    path('updateprovider/<int:provider_id>', update_provider),
    path('deleteprovider/<int:provider_id>', delete_provider),
    # service area apis url
  


]
