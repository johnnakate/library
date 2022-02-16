from datetime import date

from libtech.models import RoomReservation, SeatReservation
from libtech.forms import SeatReservationForm, RoomReservationForm


# def check_room_availability(room_name, start_time, end_time, date):
#     avail_list = []
#     date = datetime.date()
#     start_time = datetime.time()
#     end_time = datetime.time()
#     combined_start = datetime.datetime.combine(date, start_time)
#     combined_end = datetime.datetime.combine(date, end_time)
#     reservation_list = Reservation.objects.filter(room_name=room_name)
#     for reservation in reservation_list:
#         if reservation.combined_start > end_time or reservation.combined_end < start_time:
#             avail_list.append(True)
#         else:
#             avail_list.append(False)
#     return all(avail_list)

def room_availability(room, date, start_time, end_time):
    avail_list = []
    reservation_list = RoomReservation.objects.filter(room=room)
    val = RoomReservation.objects.filter(date=date).exists()

    for reservation in reservation_list:
        # if  reservation.start_time > end_time or reservation.end_time < start_time:
        if val != reservation.date != date and reservation.start_time != start_time and reservation.end_time != end_time:
            avail_list.append(True)
        # elif val == reservation.date or reservation.start_time==end_time or reservation.end_time ==start_time:
        # 	avail_list.append(False)
        else:
            avail_list.append(False)
    return all(avail_list)


def seat_availability(seat, date, start_time, end_time):
    avail_list = []
    reservation_list = SeatReservation.objects.filter(seat=seat)
    val = SeatReservation.objects.filter(date=date).exists()

    for reservation in reservation_list:

        if val != reservation.date != date and reservation.start_time != start_time and reservation.end_time != end_time:
            avail_list.append(True)
        else:
            avail_list.append(False)
        return all(avail_list)
        
# def check_seat_availability(seat_name, start_time, end_time, date):
#     avail_list = []
#     date = date.datetime.date()
#     start_time = start_time.datetime.time()
#     end_time = end_time.datetime.time()
#     combined_start = datetime.datetime.combine(date, start_time)
#     combined_end = datetime.datetime.combine(date, end_time)
#     reservation_list = Reservation.objects.filter(seat_name=seat_name)
#     for reservation in reservation_list:
#         if reservation.combined_start > end_time or reservation.combined_end < start_time:
#             avail_list.append(True)
#         else:
#             avail_list.append(False)
#     return all(avail_list)


# def seat_availability(seat_name, check_in, check_out):
#     avail_list = []
#     seatreservation_list = SeatReservation.objects.filter(seat_name=seat_name)
#     for seat in seatreservation_list:
#         if seat.check_in_seat > check_out or seat.check_out_seat < check_in:
#             avail_list.append(True)
#         else:
#             avail_list.append(False)
#     return all(avail_list)


# def room_availability(room_name, check_in, check_out):
#     avail_list = []
#     roomreservation_list = RoomReservation.objects.filter(room_name=room_name)
#     for room in roomreservation_list:
#         if room.check_in_room > check_out or room.check_out_room < check_in:
#             avail_list.append(True)
#         else:
#             avail_list.append(False)
#     return all(avail_list)
