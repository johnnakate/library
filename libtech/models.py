from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.exceptions import ValidationError
# from multiselectfield import MultiSelectField

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls.base import reverse_lazy
# from rest_framework.authtoken.models import Token

# Create your models here.

TYPES = (
    ('Room', 'Room'),
    ('Seat', 'Seat'),
)


class Room(models.Model):
    ROOM_CATEGORIES = (
        ('Pitch Room', 'PitchRoom'),
        ('Multimedia Nook', 'MultimediaNook'),
        ('Discussion Room #1', 'DiscussionRoom#1'),
        ('Discussion Room #2', 'DiscussionRoom#2'),
        ('Discussion Room #3', 'DiscussionRoom#3'),
    )
    number = models.IntegerField(
        unique=True, auto_created=True, serialize=False, null=True)
    type = models.CharField(max_length=50, choices=TYPES, null=True)
    category = models.CharField(max_length=100, choices=ROOM_CATEGORIES)

    def __str__(self):
        return f'Room Number: {self.number} || Room Category: {dict(self.ROOM_CATEGORIES)[self.category]}'

    class Meta:
        db_table = "Room"


class Room_Type(models.Model):
    room = models.ForeignKey(
        Room, blank=True, null=True, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(null=True)
    description = models.TextField(max_length=100, null=True)
    room_image = models.ImageField(upload_to='rooms', default='room.png',)

    def __str__(self):
        return f'{self.room}'

    class Meta:
        db_table = "Room_Type"


class Seat(models.Model):
    SEAT_CATEGORIES = (
        ('Activity Loft', 'ACTIVITY LOFT'),
        ('Cit-u cafe', 'CIT-U CAFE'),
        ('Collaboration Room', 'COLLABORATION ROOM'),
        ('CompuHub', 'COMPUHUB'),
        ('Activity Center', 'ACTVITY CENTER'),
        ('Elliptical', 'ELLIPTICAL AREA'),
        ('Exhibit Area', 'EXHIBIT AREA'),
        ('Filipiniana', 'FILIPIANA'),
        ('Octagon', 'OCTAGON'),
        ('Reading Duo', 'READING DUO'),
        ('Reading Hub', 'READING HUB'),
        ('Carrels', 'CARRELS')
    )

    number = models.IntegerField(
        unique=True, auto_created=True, serialize=False, null=True)
    type = models.CharField(max_length=50, choices=TYPES, null=True)
    category = models.CharField(
        max_length=50, choices=SEAT_CATEGORIES, null=True)

    def __str__(self):
        return f'Seat Number: {self.number} || Seat Category: {dict(self.SEAT_CATEGORIES)[self.category]}'

    class Meta:
        db_table = "Seat"


class Seat_Type(models.Model):
    seat = models.ForeignKey(
        Seat, on_delete=models.CASCADE, null=True, blank=True)
    capacity = models.PositiveIntegerField(null=True)
    description = models.TextField(max_length=100, null=True)
    seat_image = models.ImageField(upload_to='seats', default='seats.png')

    def __str__(self):
        return f'{self.seat}'

    class Meta:
        db_table = "Seat_Type"


class SeatReservation(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(
        Seat, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.users.username} booked seat number {self.seat.number} on {self.date} from  {self.start_time} to  {self.end_time}'

    def get_seat_category(self):
        seat_categories = dict(self.seat.SEAT_CATEGORIES)
        seat_category = seat_categories.get(self.seat.category)
        return seat_category

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError('Start Time should less than End Time')
        return super().clean()

    class Meta:
        db_table = "SeatReservation"


RESERVATION_STATUS = (
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled')
)

class RoomReservation(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.DurationField(null=True)
    status = models.CharField(max_length=50, choices=RESERVATION_STATUS, null=True)

    def __str__(self):
        return f'{self.users.username} booked room number {self.room.number} on {self.date} from  {self.start_time} to  {self.end_time}'

    def get_room_category(self):
        room_categories = dict(self.room.ROOM_CATEGORIES)
        room_category = room_categories.get(self.room.category)
        return room_category

    def get_cancel_booking_url(self):
        return reverse_lazy('CancelBookingView', args=[self.pk, ])

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError('Start Time should less than End Time')
        return super().clean()

    def duration(self):
        a, b, c, d = self.start_time.hour, self.start_time.minute, self.start_time.second, self.start_time.microsecond
        w, x, y, z = self.end_time.hour, self.end_time.minute, self.end_time.second, self.end_time.microsecond
        delt = (w-a)*60 + (x-b) + (y-c)/60. + (z-d)/60000000.
        if delt < 0:
            delt += 1440

        hh, rem = divmod(delt, 60)
        hh = int(hh)
        mm = int(rem)
        rem = (rem - mm)*60
        ss = int(rem)
        ms = (rem - ss)*1000000
        ms = int(ms)

        self.duration = '%sh %smn '
        return self.duration % (hh, mm,)

    class Meta:
        db_table = "RoomReservation"


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

# PLEASE DONT DELETE
# jus a copy of reservation form

# jame cutie hi


RESERVATION_STATUS = (
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled')
)


class Reservation(models.Model):
    room_name = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True)
    seat_name = models.ForeignKey(
        Seat, on_delete=models.CASCADE, null=True, blank=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    capacity = models.PositiveIntegerField(null=True)
    date = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    duration = models.DurationField()
    status = models.CharField(max_length=50, choices=RESERVATION_STATUS, null=True)

    def __str__(self):
        return f'{self.users}-{self.seat_name}'

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError('Start Time should less than End Time')
        return super().clean()

    def duration(self):
        a, b, c, d = self.start_time.hour, self.start_time.minute, self.start_time.second, self.start_time.microsecond
        w, x, y, z = self.end_time.hour, self.end_time.minute, self.end_time.second, self.end_time.microsecond
        delt = (w-a)*60 + (x-b) + (y-c)/60. + (z-d)/60000000.
        if delt < 0:
            delt += 1440

        hh, rem = divmod(delt, 60)
        hh = int(hh)
        mm = int(rem)
        rem = (rem - mm)*60
        ss = int(rem)
        ms = (rem - ss)*1000000
        ms = int(ms)

        self.duration = '%sh %smn '
        return self.duration % (hh, mm,)

    class Meta:
        db_table = "Reservation"

# CHOICES = (
#     ('activityloft', 'ACTIVITY LOFT'),
#     ('cit-ucafe', 'CIT-UCAFE'),
#     ('collaboration Room', 'COLLABORATIONROOM'),
#     ('compuhub', 'COMPUHUB'),
#     ('activitycenter', 'ACTVITYCENTER'),
#     ('elliptical', 'ELLIPTICALAREA'),
#     ('exhibitarea', 'EXHIBITAREA'),
#     ('filipiniana', 'FILIPIANA'),
#     ('octagon', 'OCTAGON'),
#     ('readingduo', 'READINGDUO'),
#     ('readinghub', 'READINGHUB'),
#     ('carrels', 'CARRELS')
# )

# TIME_CHOICES = (
#     ('8:00 A.M.', '8:00 A.M.'),
#     ('8:30 A.M.', '8:30 A.M.'),
#     ('9:00 A.M.', '9:00 A.M.'),
#     ('9:30 A.M.', '9:30 A.M.'),
#     ('10:00 A.M.', '10:00 A.M.'),
#     ('10:30 A.M.', '10:30 A.M.'),
#     ('11:00 A.M.', '11:00 A.M.'),
#     ('11:30 A.M.', '11:30 A.M.'),
#     ('12:00 P.M.', '12:00 P.M.'),
#     ('1:30 P.M.', '1:30 P.M.'),
#     ('2:00 P.M.', '2:00 P.M.'),
#     ('2:30 P.M.', '2:30 P.M.'),
#     ('3:00 P.M.', '3:00 P.M.'),
#     ('3:30 P.M.', '3:30 P.M.'),
#     ('4:00 P.M.', '4:00 P.M.'),
#     ('4:30 P.M.', '4:30 P.M.'),
#     ('5:00 P.M.', '5:00 P.M.'))


# ROOM_IMAGES = (
#         ('Pitch Room', 'PitchRoom'),
#         ('Multimedia Nook', 'MultimediaNook'),
#         ('Discussion Room #1', 'DiscussionRoom#1'),
#         ('Discussion Room #2', 'DiscussionRoom#2'),
#         ('Discussion Room #3', 'DiscussionRoom#3'),
#     )

# SEAT_IMAGES = (
#         ('Activity Loft', 'ACTIVITY LOFT'),
#         ('Cit-u cafe', 'CIT-U CAFE'),
#         ('Collaboration Room', 'COLLABORATION ROOM'),
#         ('CompuHub', 'COMPUHUB'),
#         ('Activity Center', 'ACTVITY CENTER'),
#         ('Elliptical', 'ELLIPTICAL AREA'),
#         ('Exhibit Area', 'EXHIBIT AREA'),
#         ('Filipiniana', 'FILIPIANA'),
#         ('Octagon', 'OCTAGON'),
#         ('Reading Duo', 'READING DUO'),
#         ('Reading Hub', 'READING HUB'),
#         ('Carrels', 'CARRELS')
#     )
