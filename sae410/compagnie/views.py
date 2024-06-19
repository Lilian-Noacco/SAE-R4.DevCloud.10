from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Vol, Reservation, Achat
from .serializer import AchatSerializer, VolSerializer, ReservationSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
import nats
from . import nats_utils
import asyncio
import json


@csrf_exempt
@api_view(['GET', 'POST'])  # Il faudra enlever le post, on ne veut pas que des gens lambas puissent ajouter des vols...
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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
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


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication,
                         TokenAuthentication])  # remarque : ces classes sont nécessaires pour récupérer le nom avec request.user
@permission_classes([IsAuthenticated])
def reservation_list(request):  # Faire en sorte d'afficher en fonction de l'utilisateur
    if request.method == 'GET':
        reservations = Reservation.objects.filter(reservation_nom=request.user.id)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        print(request.user)
        print(request.user.id)


        data = JSONParser().parse(request)
        data['reservation_nom'] = request.user.id
        serializer = ReservationSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.reservation_nom = request.user
        print(serializer.reservation_nom)
        serializer.save()

        v = Vol.objects.get(pk=data["reservation_vol"])
        if v.vol_place_restante > int(data["reservation_nombre_personne"]):
            v.vol_place_restante -= int(data["reservation_nombre_personne"])
            v.save()
        else:
            return Response({"res": "Nombre de places restantes insuffisante"}, status=status.HTTP_400_BAD_REQUEST)


        client_email = request.user.email
        client_nb_place = data["reservation_nombre_personne"]
        corp_mail = f"Chèr(e) {request.user.first_name}, votre réservation de {client_nb_place} place(s) à bien été prise en compte! Merci d'avoir choisi Airflow"

        send_mail(
            "Confirmation de votre réservation",
            corp_mail,
            "airflow.rtproject@gmail.com",
            [client_email],
        )

        return Response({"res": "Reservation OK"}, status=201)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@csrf_exempt
def reservation_detail(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ReservationSerializer(reservation, data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(serializer.data, status=201)


    elif request.method == 'DELETE':
        reserv = Reservation.objects.get(pk=pk)
        v = reserv.reservation_vol

        v.vol_place_restante += reserv.reservation_nombre_personne
        v.save()
        reserv.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET', 'POST'])
def achat_list(request):  # Faire en sorte d'afficher en fonction de l'utilisateur
    if request.method == 'GET':
        achats = Achat.objects.all()
        serializer = AchatSerializer(achats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AchatSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        paiement = asyncio.run(nats_utils.request_message("pay", f"{data['achat_iban']},{data['achat_montant']}",
                                                          "nats://172.24.27.223:4222"))
        print(paiement)
        if paiement == "True":
            serializer.save()
            return Response("SUCCES : Somme preleve sur compte", status=201)
        return Response({"res": "ECHEC : Paiement Refuse"}, status=201)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@csrf_exempt
def achat_detail(request, pk):
    try:
        achat = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AchatSerializer(achat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AchatSerializer(achat, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        achat.delete()
        return HttpResponse(status=204)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    print(request.user)
    return Response("passed!")
