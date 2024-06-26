from rest_framework import serializers
from .models import Vol, Reservation, Achat
from django.contrib.auth import get_user_model

UserModel = get_user_model()
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user
    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password", "first_name", "last_name", "email")

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
