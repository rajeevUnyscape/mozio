from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient
from djgeojson.fields import PolygonField
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Provider, ServiceArea
from .serializers import ServiceAreaSerializer
from random import randint
import json
from django.conf import settings
from geojson import Polygon
from django.test import TestCase
from django.core import exceptions


P1 = Polygon([
    [3.20, 25.29],
    [21.08, 2.34],
    [18.57, 1.87],
    [-8.69, 5.43],
    [-5.72, -8.04],
    [-2.86, 3.11],
    [-9.35, 4.43],
    [-8.87, 11.61],
    [2.10, 12.19]
])

P2 = Polygon([
    [6.17, 3.27],
    [1.80, 9.76],
    [4.75, 5.56],
    [2.85, 2.56],
    [5.83, 11.49],
    [6.61, 22.46],
    [3.52, 15.26]
])


class ModelMixin:

    def create_user(self, username=None, password= None, email= None):
        if not username:
            username = str(get_random_string())
        if not password:
            password = "Rajeev@123"
        if not email:
            email = get_random_string() + "@gmail.com"
        return User.objects.create_user(username=username,
                                 email=str(email),
                                 password=password)

    def create_provider(self, name=None, email=None, language=None,
                        currency=None,created_by = None,updated_by= None,description=None ):
        if not name:
            name = get_random_string()
        if not email:
            email = get_random_string() + "@gmail.com"
        if not language:
            language = "eng"
        if not currency:
            currency = "dollar"
        if not description:
            description = get_random_string()
        if not created_by:
            created_by = self.create_user()
        if not updated_by:
            updated_by = self.create_user()
        provider =  Provider.objects.create(
            name=str(name), language=str(language), email=str(email),
            currency=str(currency),created_by =created_by ,updated_by=updated_by,description=description)
        return provider

    def create_service_area(self, geom=None, provider=None, name=None,
                            price=None,created_by= None,updated_by= None,description=None):
        if not geom:
            geom = Polygon([
                    [9.57, 14.26],
                    [14.90, 5.67],
                    [3.88, 4.68],
                    [16.50, 4.69],
                    [14.83, 13.22],
                    [4.14, 12.23],
                    [3.75, 11.24]
                ])
        if not provider:
            provider = self.create_provider()
        if not name:
            name = get_random_string()
        if not price:
            price = str(randint(1, 1000))
        if not description:
            description = get_random_string()
        if not created_by:
            created_by = self.create_user()
        if not updated_by:
            updated_by = self.create_user()
        return ServiceArea.objects.create(
            geom=geom, provider=provider,
            name=str(name), price=str(price),created_by =created_by ,updated_by=updated_by,description=description)


class TestModels(ModelMixin, TestCase):
    def test_create_provider_and_two_equal_areas(self):
        provider = self.create_provider()
        geom = {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        0,
                        0
                    ],
                    [
                        3,
                        6
                    ],
                    [
                        6,
                        1
                    ],
                    [
                        0,
                        0
                    ]
                ]
            ]
        }
        area1 = self.create_service_area(geom, provider=provider)
        area2 = self.create_service_area(geom, provider=provider)
        self.assertEqual(area1.provider, provider)
        self.assertEqual(area2.provider, provider)
        self.assertEqual(area2.geom, area1.geom)


class TestSerializers(ModelMixin, TestCase):
    def test_serialize_service_area(self):
        name = get_random_string()
        email = name + '@gmail.com'
        language = 'eng'
        currency = 'dollar'
        provider = self.create_provider(name=name, email=email, language=language, currency=currency)
        area = self.create_service_area(name=name, provider=provider, price=100)
        serializer = ServiceAreaSerializer(area)


class TestAPI(ModelMixin, TestCase):
    client_class = APIClient

    def test_providers(self):
        r = self.client.get('/provider/')
        self.assertEqual(r.status_code, 200)

    def test_service_areas(self):
        r = self.client.get('/serviceArea/')
        self.assertEqual(r.status_code, 200)

    def test_create_providers(self):
        user = self.create_user()
        r = self.client.post('/provider/', {'name': 'test',
                                            'email' : 'abc@gmail.com',
                                            'language': "language",
                                            "currency":"currency",
                                            "phone_number":"phone_number",
                                            "description":"description",
                                            "created_by_id":user.id,
                                            "updated_by_id":user.id})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.count(), 1)
        self.assertEqual(Provider.objects.get().name, 'test')

    def test_create_service_areas(self):
        provider = self.create_provider()
        r = self.client.post('/serviceArea/', {
            'geom':json.dumps({
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                0,
                                0
                            ],
                            [
                                3,
                                6
                            ],
                            [
                                6,
                                1
                            ],
                            [
                                0,
                                0
                            ]
                        ]
                    ]
                }),
            'provider_id': provider.id,
            'name': 'test',
            'description':'description',
            'created_by': self.create_user(),
            'updated_by': self.create_user()})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceArea.objects.count(), 1)
        self.assertEqual(ServiceArea.objects.get().name, 'test')

    def test_list_providers(self):
        providers = [self.create_provider() for _ in range(20)]
        r = self.client.get('/provider/')
        self.assertEqual(r.status_code, 200)

    def test_list_service_areas(self):
        areas = [self.create_service_area() for _ in range(20)]
        r = self.client.get('/serviceArea/')
        self.assertEqual(r.status_code, 200)
     

    def test_service_areas_filter_by_provider_id(self):
        s1 = self.create_service_area(P1)
        s2 = self.create_service_area(P2)
        [self.create_service_area(provider=s2.provider) for _ in range(10)]

        filters = 'provider_id=' + str(s1.provider_id)
        r = self.client.get('/serviceArea/?' + filters)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

        filters = 'provider_id=' + str(s2.provider_id)
        r = self.client.get('/serviceArea/?' + filters)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 11)

    def test_service_areas_filter_by_geom_contains(self):
        s1 = self.create_service_area(P1)
        s2 = self.create_service_area(P2)
        [self.create_service_area() for _ in range(10)]

        filters = 'geom__contains={"type":"Point","coordinates":' \
                  '[9.26,10.56]}'
        r = self.client.get('/serviceArea/?' + filters)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

    def test_areas_filter_by_geom_contains_and_provider_id(self):
        s1 = self.create_service_area(P1)
        self.create_service_area(P2)
        [self.create_service_area() for _ in range(10)]

        filters = 'geom__contains={"type":"Point","coordinates":' \
                  '[9.26,10.56]}'
        filters += '&provider_id=' + str(s1.provider_id)
        r = self.client.get('/serviceArea/?' + filters)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

    def test_areas_filter_format_error(self):
        [self.create_service_area() for _ in range(10)]

        filters = 'geom__contains={"type":"Point","coordinates":' \
                  '[9.26,10.56]}'
        r = self.client.get('/serviceArea/?' + filters)
        self.assertEqual(r.status_code, 200)