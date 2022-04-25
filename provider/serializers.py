from rest_framework import serializers
from .models import Provider, ServiceArea
from django.contrib.auth.models import User
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.relations import PrimaryKeyRelatedField


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']

class ProviderSerializer(serializers.ModelSerializer):
    created_by  = serializers.CharField(read_only=True)
    updated_by = serializers.CharField(read_only=True)
    class Meta:
        model = Provider
        fields = ['id','name', 'language', 'currency', 'phone_number','created_date','updated_date','created_by','updated_by']

class ServiceAreaSerializer(GeoFeatureModelSerializer):
    provider = ProviderSerializer(read_only=True)
    provider_id = PrimaryKeyRelatedField(queryset=Provider.objects.all(),required=True, write_only=True, source='provider')
    class Meta:
        model = ServiceArea
        geo_field = "geom"
        fields = ('id', 'name', 'provider', 'provider_id', 'price')
        auto_bbox = True

