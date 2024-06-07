from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Vol, Reservation, Achat
from .serializer import AchatSerializer, VolSerializer, ReservationSerializer
from rest_framework.response import Response
from rest_framework import status
import json
@csrf_exempt
@api_view(['GET','POST'])
def vol_list(request):
    if request.method == 'GET':
        vols = Vol.objects.all()
        serializer = VolSerializer(vols, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VolSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET','PUT','PATCH','DELETE'])
@csrf_exempt
def vol_detail(request, pk):
    try:
        vol = Vol.objects.get(pk=pk)
    except Vol.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = VolSerializer(vol)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = VolSerializer(vol, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        vol.delete()
        return HttpResponse(status=204)
