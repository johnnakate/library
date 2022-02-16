from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from libtech.models import *
from libtech.api.serializers import *

@api_view(['POST',])
def registration_view(request):
	if request.method == 'POST':
		serializer = RegisterSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			token = Token.objects.get_or_create(user=account)
			data['token'] = str(token)
		else:
			data = serializer.errors
		return Response(data)
        
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getReservations(request,pk):
	reservations = RoomReservation.objects.get(users_id=pk)
	serializers = RoomReservationSerializer(reservations, many= True)
	return Response(reservations)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createRoomReservations(request):
	serializer = RoomReservationSerializer(data=request.data)
	user = request.user
	data = {}
	if serializer.is_valid():
		reservation = serializer.save()
		data['response'] = 'Successfully reserved.'
		data['room_id'] = reservation.room_id
		data['users_id'] = reservation.users_id
		data['date'] = user.date
		data['start_time'] = reservation.start_time
		data['end_time'] = reservation.end_time
	else:
		data = serializer.errors
	return Response(data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createSeatReservations(request):
	serializer = SeatReservationSerializer(data=request.data)
	user = request.user
	data = {}
	if serializer.is_valid():
		reservation = serializer.save()
		data['response'] = 'Successfully reserved.'
		data['seat_id'] = reservation.seat_id
		data['users_id'] = user.id
		data['date'] = reservation.date
		data['start_time'] = reservation.start_time
		data['end_time'] = reservation.end_time
	else:
		data = serializer.errors
	return Response(data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getRooms(request):
	rooms = Room.objects.all()
	serializers = RoomSerializer(rooms, many= True)
	return Response(rooms)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getSeats(request):
	seats = Seat.objects.all()
	serializers = SeatSerializer(seats, many= True)
	return Response(seats)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getToken(request):
	authtoken = Token.objects.all()
	serializers = SeatSerializer(authtoken, many= True)
	return Response(authtoken)