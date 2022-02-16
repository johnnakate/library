from django.contrib.auth.models import User
from django import forms
from .models import Room, Seat, Room_Type, Seat_Type, RoomReservation, SeatReservation

from .models import *

class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = '__all__'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = Room_Type
        fields = ['capacity', 'description', 'room_image']

class SeatTypeForm(forms.ModelForm):
    class Meta:
        model = Seat_Type
        fields = ['capacity', 'description', 'seat_image']


class AvailabilityForm(forms.Form):
    # date = forms.DateField(
    #     required=True, input_formats=["%d-%m-%Y", ])
    date = forms.DateField(
        required=True)
    start_time = forms.TimeField(
        required=True, input_formats=["%H:%M", ])
    end_time = forms.TimeField(
        required=True, input_formats=["%H:%M", ])
    # start_time = forms.DateTimeField(
    #     required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    # end_time = forms.DateTimeField(
    #     required=True, input_formats=["%Y-%m-%dT%H:%M", ])


class RoomReservationForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }
        
        fields = ["date", "start_time", "end_time"]

class SeatReservationForm(forms.ModelForm):
    class Meta:
        model = SeatReservation
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),}

        fields = ["date", "start_time", "end_time"]

class ReservationForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time'}))
    # , input_formats=["%H:%M", ]
    # room_name = forms.ModelChoiceField(
    #     queryset=Room.objects.all(), empty_label="Choose Room", required=False)
    seat_name = forms.ModelChoiceField(
        queryset=Seat.objects.all(), empty_label="Choose Area", required=False)

    class Meta:
        model = Reservation
        fields = ['date', 'start_time',
                  'end_time', 'capacity', ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control'}),
            # 'room_name': forms.ModelChoiceField(queryset=Room.objects.filter(room_name=room_name))
            # 'room_name': forms.ModelChoiceField(required=False, queryset=Room.room_name, empty_label="Choose Room")
        }

        # def clean(self):
        #     all_clean_data = super().clean()
        #     start_time = all_clean_data['start_time']
        #     end_time = all_clean_data['end_time']
        #     date = all_clean_data['date']

        #     if date < start_time or date > end_time:
        #         raise forms.ValidationError("Please Enter a valid date")

    # def clean_end_date(self, *args, **kwargs):
    #     start_time = self.cleaned_data['start_time']
    #     end_time = self.cleaned_data['end_time']

    #     if end_time <= start_time:
    #         raise forms.ValidationError(
    #             "End date must be later than start date")

    #     # Always return a value to use as the new cleaned data, even ifb this method didn 't change it.
    #     return super(ReservationForm, self).save(*args, **kwargs)
    # start_time = forms.TimeField(label = 'Start time', label_suffix = " : ",
    # required = True, disabled = False, input_formats = ["%H:%M:%S"],
    #     widget=forms.TimeInput(attrs={'type': 'time'}))

    # validation for time
    # def validatetime(self):
    #     this_period_end = self.start_time + \
    #         datetime.timedelta(hours=self.duration)
    #     existing_reservations = self.reservation_set.filter(
    #         start_time__lt=this_period_end,
    #         end_time__gte=self.start_time
    #     )
    #     raise forms.ValidationError(
    #         "End time should be greater than Start Time")
    # print(validatetime)
