from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProviderSerializer,ServiceAreaSerializer
from .models import Provider,ServiceArea
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework_gis.pagination import GeoJsonPagination



#  PROVIDER APIS

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])  
def welcome(request):
    content = {"message": "Welcome to the Mozio!"}
    return JsonResponse(content)


class get_provider_with_page(viewsets.ViewSet):
    def list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 2
        provider_objects = Provider.objects.all()
        result_page = paginator.paginate_queryset(provider_objects, request)
        serializer = ProviderSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_provider(request):
    user = request.user.id
    providers = Provider.objects.filter(created_by=user)
    serializer = ProviderSerializer(providers, many=True)
    return JsonResponse({'Providers': serializer.data,"email":user.email}, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_providers(request):
    payload = json.loads(request.body)
    user = request.user
    try:
        user = User.objects.get(id=user.id)
        provider = Provider.objects.create(
            name=payload["name"],
            language=payload["language"],
            currency=payload["currency"],
            phone_number=payload["phone_number"],
            created_by=user,
            updated_by=user
        )
        serializer = ProviderSerializer(provider)
        return JsonResponse({'provider': serializer.data,"email": user.email}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_provider(request, provider_id):
    user = request.user.id
    payload = json.loads(request.body)
    try:
        provider = Provider.objects.filter(created_by=user, id=provider_id)
        provider.update(**payload)
        providers = Provider.objects.get(id=provider_id)
        providers.updated_date = timezone.now()
        providers.save()
        serializer = ProviderSerializer(providers)
        return JsonResponse({'provider': serializer.data, "email":user.email}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_provider(request, provider_id):
    user = request.user.id
    try:
        provider = Provider.objects.get(created_by=user, id=provider_id)
        provider.delete()
        return JsonResponse({'status': "Deleted"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#  SERVICE AREA APIS

class ServiceAreaViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all()
    pagination_class = GeoJsonPagination

    def get_queryset(self):
        queryset = ServiceArea.objects.all()
        provider_id = self.request.query_params.get('provider_id', None)
        if provider_id is not None:
            if not provider_id.isdigit():
                raise exceptions.ValidationError('invalid provider_id')
            queryset = queryset.filter(provider_id=int(provider_id))
        geom_contains = self.request.query_params.get('geom__contains', None)
        if geom_contains is not None:
            try:
                data = json.loads(geom_contains)
                data_coordinates = [float(x) for x in data['coordinates']]
                data_type = data['type']
                if data_type != "Point":
                    raise ValueError('invalid type! only Point type allowed')
                if len(data_coordinates) != 2:
                    raise ValueError('wrong coordinates length')
                pnt_wkt = 'POINT(%s)' % ' '.join(map(str, data_coordinates))
            except (ValueError, KeyError, TypeError) as e:
                raise exceptions.ValidationError(
                    'invalid geom__contains: %s' % e)
            queryset = queryset.filter(geom__contains=pnt_wkt)
        return queryset








