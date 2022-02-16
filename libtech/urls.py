from django.conf.urls import include
from django.urls import path, reverse_lazy
from .import views
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required

from .views import RoomDetailView, RoomListView, SeatDetailView, SeatListView


#from rest_framework.authtoken.views import obtain_auth_token
#from .views import *

urlpatterns = [
    path('landing/', views.landing, name='landing'),
    path('accountsettings/', user_views.settings_account, name='settings-account'),
    #path('passwordsettings/', user_views.settings_pass, name='settings-pass'),

    path('change_password/', PasswordChangeView.as_view(
        template_name='settings/change_password.html',
        success_url=reverse_lazy('password_change_done')
    ),
        name='password_change'),

    path('change_password/done/', PasswordChangeDoneView.as_view(
        template_name='settings/change_password_done.html'),
        name='password_change_done'),


    path('dashboard/', views.index, name='admin-dashboard'),
    path('analytics/', user_views.analytics_view, name='admin-analytics'),

    path('roomview/', views.room_view, name='room-view'),
    path('room/edit/<int:pk>/', views.room_edit, name='room-edit'),
    path('room/delete/<int:pk>/', views.room_delete, name='room-delete'),

    path('userdetail/', views.user_detail, name='user-detail'),
    path('user/view/<int:pk>/', views.user_view, name='user-view'),

    path('addreservation/', views.add_reservation, name='add-reservation'),
    path('reservationview/', views.reservation_view, name='reservation-view'),
    path('reservation/edit/<int:pk>/',
         views.reservation_edit, name='reservation-edit'),
    path('reservation/delete/<int:pk>/',
         views.reservation_delete, name='reservation-delete'),

    path('seatview/', views.seat_view, name='seat-view'),
    path('seat/edit/<int:pk>/', views.seat_edit, name='seat-edit'),
    path('seat/delete/<int:pk>/', views.seat_delete, name='seat-delete'),

    path('reservation_list/', views.reservation_list, name='reservation_list'),
    # path('reservationdetail/<int:pk>/', views.reservation_detail, name='reservation_detail'),

    path('type/', views.reservation_type, name="reservation_type"),
    path('type/seat', views.seat_list, name='seat_list'),
    path('type/room', views.room_list, name='room_list'),

    path('seat_list/', SeatListView, name='SeatListView'),
    path('reservationseaterror/', views.ReservationSeatError, name='ReservationSeatError'),
    # path('reservationlist/', login_required(BookingListView.as_view()),
    #      name='BookingListView'),
    path('seat/<category>', login_required(SeatDetailView.as_view()), name='SeatDetailView'),


    path('room_list/', RoomListView, name='RoomListView'),
    path('reservationroomerror/', views.ReservationRoomError, name='ReservationRoomError'),
    path('room/<category>', login_required(RoomDetailView.as_view()), name='RoomDetailView'),


    # path('booking/edit/<id>', update_view,name='EditBookingView'),
    # path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    # path('', views.home, name='home')



    # path('forgotpassword/', user_views.forgot_password, name='forgot-password'),
    # path('changepassword/<token>', user_views.change_password, name='change-password'),

    #   MOBILE
    #   path('login/', obtain_auth_token),
    #   path('register/', Registernow.as_view()),
    path('api/', include('libtech.api.urls', 'libtech_api')),
]
