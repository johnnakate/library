# from django.contrib import admin
# from .models import User

# Register your models here.
# admin.site.register(User)

from django.contrib import admin
from .models import Room, Room_Type, RoomReservation, Seat, Reservation, SeatReservation

admin.site.site_header = 'LibTech Admin Panel'

# Register your models here.
admin.site.register(Room)
admin.site.register(Room_Type)
admin.site.register(Seat)
admin.site.register(Reservation)
admin.site.register(SeatReservation)
admin.site.register(RoomReservation)
