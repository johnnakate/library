from collections import UserDict
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Room, Room_Type, RoomReservation, Seat, SeatReservation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, View, DeleteView
# from .decorators import auth_users, allowed_users
# from .filters import ReservationFilter


from libtech.functions.availability import room_availability, seat_availability
#from libtech.functions.total_reserve import check_duration
from django.http.response import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import *
from .forms import RoomForm, RoomReservationForm, RoomTypeForm, SeatForm, ReservationForm, SeatReservationForm, AvailabilityForm, SeatTypeForm



def landing(request):
    return render(request, 'landing.html')


@login_required(login_url='login')
def index(request):
    reservations = RoomReservation.objects.all()
    room_type = Room_Type.objects.all()
    seat_type = Seat_Type.objects.all()
    room = Room.objects.all()
    seat = Seat.objects.all()

    res = RoomReservation.objects.filter(users=request.user)
    res_count = res.count()
    current_res = RoomReservation.objects.filter(
        users=request.user, date=date.today()).count()

    users_count = User.objects.all().count()
    reservations_count = reservations.count()
    rooms_count = room.count()
    seats_count = seat.count()

    today = date.today()
    foot_traffic = RoomReservation.objects.filter(date=date.today()).count()

    # resFilter = ReservationFilter()

    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.users = request.user
            instance.save()
            return redirect('admin-dashboard')
        elif 'btnCancel' in request.POST:
                form = RoomReservationForm(request.POST)
                form.status = 'CANCELLED'
                form.save()          
    else:
        form = RoomReservationForm()
    context = {
        'reservations': reservations,
        'form': form,
        'room_type': room_type,
        'seat_type': seat_type,
        'room': room,
        'seat': seat,

        'users_count': users_count,
        'reservations_count': reservations_count,
        'rooms_count': rooms_count,
        'seats_count': seats_count,

        'today': today,
        'foot_traffic': foot_traffic,

        'res': res,
        'res_count': res_count,
        'current_res': current_res,

        # 'resFilter': resFilter,
    }
    return render(request, 'administrator_dashboard.html', context)


@login_required(login_url='login')
def add_reservation(request):
    # room_name = self.kwargs.get('room_name', None)
    reservations = Reservation.objects.all()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.users = request.user
            instance.save()
            return redirect('admin-dashboard')
    else:
        form = ReservationForm()
    context = {
        'form': form,
    }
    return render(request, 'add_reservation.html', context)



@login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin'])
def user_detail(request):
    users = User.objects.all()

    users_count = users.count()
    reservations_count = RoomReservation.objects.all().count()
    rooms_count = Room.objects.all().count()
    seats_count = Seat.objects.all().count()

    context = {
        'users': users,
        'users_count': users_count,
        'reservations_count': reservations_count,
        'rooms_count': rooms_count,
        'seats_count': seats_count,
    }
    return render(request, 'user/user_detail.html', context)


@login_required(login_url='login')
def user_view(request, pk):
    users = User.objects.get(id=pk)
    context = {
        'users': users,
    }
    return render(request, 'user/user_view.html', context)


@login_required(login_url='login')
def room_view(request):
    room = Room.objects.all()
    room_type = Room_Type.objects.all()

    users_count = User.objects.all().count()
    reservations_count = RoomReservation.objects.all().count()
    rooms_count = room.count()
    seats_count = Seat.objects.all().count()
    zipped_data = zip(room, room_type)

    if request.method == 'POST':
        form = RoomForm(request.POST)
        form2 = RoomTypeForm(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            # Get the current instance object to display in the template
            img_obj = form2.instance
            category = form.cleaned_data.get('category')
            messages.success(request, f'{category} has been added')
            # return render(request, 'room/room_view.html', {'form': form, 'img_obj': img_obj})
            return redirect('room-view')
    else:
        form = RoomForm()
        form2 = RoomTypeForm()
    context = {
        'room': room,
        'room_type': room_type,
        'form': form,
        'form2': form2,
        'users_count': users_count,
        'reservations_count': reservations_count,
        'rooms_count': rooms_count,
        'seats_count': seats_count,
        'zipped_data': zipped_data,

    }
    return render(request, 'room/room_view.html', context)


login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin'])


def room_edit(request, pk):
    item = Room.objects.get(id=pk)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            return redirect('room-view')
    else:
        form = RoomForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'room/room_edit.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin'])
def room_delete(request, pk):
    item = Room.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('room-view')
    context = {
        'item': item
    }
    return render(request, 'room/room_delete.html', context)
# views for seats


@login_required(login_url='login')
def seat_view(request):
    seat = Seat.objects.all()
    seat_type = Seat_Type.objects.all()

    users_count = User.objects.all().count()
    reservations_count = RoomReservation.objects.all().count()
    rooms_count = Room.objects.all().count()
    seats_count = seat.count()
    zipped_data = zip(seat, seat_type)

    if request.method == 'POST':
        form = SeatForm(request.POST)
        form2 = SeatTypeForm(request.POST)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            # img_obj = form2.instance
            category = form.cleaned_data.get('category')
            messages.success(request, f'{category} has been added')
            return redirect('seat-view')
    else:
        form = SeatForm()
        form2 = SeatTypeForm()
    context = {
        'seat': seat,
        'form': form,
        'form2': form2,
        'users_count': users_count,
        'reservations_count': reservations_count,
        'rooms_count': rooms_count,
        'seats_count': seats_count,
        'seat_type': seat_type,
        'zipped_data': zipped_data,
    }
    return render(request, 'seat/seat_view.html', context)


login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin'])


def seat_edit(request, pk):
    item = Seat.objects.get(id=pk)
    if request.method == 'POST':
        form = SeatForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('seat-view')
    else:
        form = SeatForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'seat/seat_edit.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin'])
def seat_delete(request, pk):
    item = Seat.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('seat-view')
    context = {
        'item': item
    }
    return render(request, 'seat/seat_delete.html', context)


@login_required(login_url='login')
def reservation_view(request):
    reservations = RoomReservation.objects.all()

    users_count = User.objects.all().count()
    reservations_count = reservations.count()
    rooms_count = Room.objects.all().count()
    seats_count = Seat.objects.all().count()

    context = {
        'reservations': reservations,
        'users_count': users_count,
        'reservations_count': reservations_count,
        'rooms_count': rooms_count,
        'seats_count': seats_count,
    }

    return render(request, 'reservation_view.html', context)


def reservation_edit(request, pk):
    item = Reservation.objects.get(id=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('reservation-view')
    else:
        form = ReservationForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'reservation/reservation_edit.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin'])
def reservation_delete(request, pk):
    item = Reservation.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('reservation-view')
    context = {
        'item': item
    }
    return render(request, 'reservation/reservation_delete.html', context)

@login_required(login_url='login')
def reservation_type(request):
    return render(request, 'temp/choose_type.html')

@login_required(login_url='login')
def reservation_list(request):
    return render(request, 'user/reservation_list.html')

@login_required(login_url='login')
def reservation_detail(self, request, pk):
    room = Room.objects.get(id=pk)
    #seat = Seat.objects.get(id=pk)
    #room_list = Room.objects.get(type=type)
    #available_to_reserve = []
    category = self.kwargs.get('category', None)

    #form = SeatRoomForm()
    # seatroom_list = SeatRoom.objects.filter(category)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=room)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.users = request.user
            instance.save()
            return redirect('admin-dashboard')
    else:
        form = ReservationForm(instance=room)
    context = {
        # 'room': room,
        'form': form,
        # 'seat': seat,
    }
    return render(request, 'user/reservation_detail.html', context)

@login_required(login_url='login')
def room_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'temp/roomlist.html', context)

@login_required(login_url='login')
def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)

    rooms = Room.objects.all()[0]
    room_type = Room_Type.objects.filter(room=rooms)

    room_description = Room_Type.description
    room_values = room_categories.values()
    room_list = []

    if len(room_type) >0 :
        # rooms = room_list[0]
        room_type = Room_Type.objects.filter(room=rooms)

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('RoomDetailView', kwargs={
                           'category': room_category})

        room_list.append((room, room_url))
        # print(room_list)


    context = {
        'room_list': room_list,
        'room_type': room_type,
    }
    return render(request, 'temp/roomlist.html', context)


class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)
        rooms = Room.objects.all()[0]
        room_type = Room_Type.objects.filter(room=rooms)
        
        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)

            if len(room_type) >0 :
                rooms = room_list[0]
                room_type = Room_Type.objects.filter(room=rooms)
                
            context = {
                'room_category': room_category,
                'form': form,
                # 'rooms': rooms,
                'room_type': room_type,
            }
            return render(request, 'temp/room_detail.html', context)
        else:
            # return HttpResponse('Category does not exist')
            return render(request, 'temp/roomcategory_error.html')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if room_availability(room, data['date'], data['start_time'], data['end_time']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = RoomReservation.objects.create(
                users=self.request.user,
                room=room,
                date=data['date'],
                start_time=data['start_time'],
                end_time=data['end_time']
            )
            booking.status = 'CONFIRMED'
            booking.date = datetime.now()
            booking.save()

            return redirect('admin-dashboard')
        else:
            return redirect('ReservationRoomError')
            # return render(request, 'temp/error.html')
            # return HttpResponse('All of this category of tables are booked!! Try another one')

@login_required(login_url='login')
def seat_list(request):
    seats = Seat.objects.all()
    context = {
        'seats': seats
    }
    return render(request, 'temp/seatlist.html', context)

@login_required(login_url='login')
def SeatListView(request):
    seat = Seat.objects.all()
    seat_categories = dict(seat.SEAT_CATEGORIES)

    seat_description = Seat_Type.description
    seat_values = seat_categories.values()
    seat_list = []

    for seat_category in seat_categories:
        seat = seat_categories.get(seat_category)
        seat_url = reverse('SeatDetailView', kwargs={
                           'category': seat_category})

        seat_list.append((seat, seat_url))
        # print(seat_list)
    context = {
        "seat_list": seat_list,
    }
    return render(request, 'temp/seatlist.html', context)


class SeatDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        seat_list = Seat.objects.filter(category=category)

        seats = Seat.objects.all()[0]
        seat_type = Seat_Type.objects.filter(seat=seats)

        if len(seat_list) > 0:
            seat = seat_list[0]
            seat_category = dict(seat.SEAT_CATEGORIES).get(seat.category, None)

            if len(seat_type) >0 :
                seats = seat_list[0]
                seat_type = Seat_Type.objects.filter(seat=seats)

            context = {
                'seat_category': seat_category,
                'form': form,
                'seat_type': seat_type,
            }
            return render(request, 'temp/seat_detail.html', context)
        else:
            # return HttpResponse('Category does not exist')
            return render(request, 'temp/seatcategory_error.html')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        seat_list = Seat.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_seats = []
        for seat in seat_list:
            if seat_availability(seat, data['date'], data['start_time'], data['end_time']):
                available_seats.append(seat)

        if len(available_seats) > 0:
            seat = available_seats[0]
            booking = SeatReservation.objects.create(
                users=self.request.user,
                seat=seat,
                date=data['date'],
                start_time=data['start_time'],
                end_time=data['end_time']
            )

            booking.save()
            return redirect('admin-dashboard')
        else:
            return redirect('ReservationSeatError')

@login_required(login_url='login')
def ReservationRoomError(request):
    room = Room.objects.all()
    room2 = RoomReservation.objects.all()
    zipped_data = zip(room, room2)
    context = {
        'room': room,
        'room2': room2,
        'zipped_data': zipped_data,
    }
    return render(request, 'temp/reservationtype_error.html', context)

@login_required(login_url='login')
def ReservationSeatError(request):
    seat = Seat.objects.all()
    seat2 = SeatReservation.objects.all()
    zipped_data = zip(seat, seat2)
    context = {
        'seat': seat,
        'seat2': seat2,
        'zipped_data': zipped_data,
    }
    return render(request, 'temp/seatreservationtype_error.html', context)
