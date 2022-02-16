from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from libtech.models import RoomReservation, Room, Seat
from user.models import *


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password','password2')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = User(
            email=self.validated_data['email'],
					username=self.validated_data['username']
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

#Seat Reservation Serializer
class SeatReservationSerializer(ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = '__all__'

#Room Reservation Serializer
class RoomReservationSerializer(ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = '__all__'

#Seat Serializer
class SeatSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

#Room Serializer
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

#Profile Serializer
class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

#User Serializer
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#Token Serializer
class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'