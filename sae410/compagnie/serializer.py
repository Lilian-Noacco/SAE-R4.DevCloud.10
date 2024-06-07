from rest_framework import serializers
from .models import Vol, Reservation, Achat


class AchatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achat
        fields = "__all__"
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
class VolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vol
        fields = "__all__"
