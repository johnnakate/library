from django.urls import path
from libtech.api import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'libtech'

urlpatterns = [
	path('register/', views.registration_view, name="register"),
	path('login/', obtain_auth_token, name="login"),
	path('reservations/<str:pk>/', views.getReservations, name="getReservation"),
	path('reservations/create/room', views.createRoomReservations, name="createReservation"),
	path('reservations/create/seat', views.createSeatReservations, name="createReservation"),
	path('rooms/', views.getRooms, name="getRooms"),
	path('seats/', views.getSeats, name="getSeats"),

	path('authToken/', views.getToken, name="tokenModel"),
]
