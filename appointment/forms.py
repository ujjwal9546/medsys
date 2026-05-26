from django import forms
from .models import Appointment
from datetime import date, datetime


class AppointmentForm(forms.ModelForm):

    def __init__(self, *args, doctor=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.doctor = doctor


    class Meta:

        model = Appointment

        fields = [

            'date',
            'time',
            'reason'

        ]


        widgets = {

            'date': forms.DateInput(

                attrs={

                    'type': 'date',

                    'min': date.today().isoformat()

                }

            ),

            'time': forms.TimeInput(

                attrs={

                    'type': 'time'

                }

            )

        }


    def clean(self):

        cleaned = super().clean()

        d = cleaned.get('date')

        t = cleaned.get('time')


        if not d or not t:

            return cleaned


        # prevent past dates

        if d < date.today():

            raise forms.ValidationError(

                "Past date not allowed"

            )


        # prevent past time today

        if d == date.today():

            if t < datetime.now().time():

                raise forms.ValidationError(

                    "Past time not allowed"

                )


        # doctor availability check

        if self.doctor:


            weekday = d.strftime('%a')


            available = []


            if self.doctor.available_days:

                available = [

                    x.strip()

                    for x in

                    self.doctor.available_days.split(',')

                ]


            # doctor never selected days

            if not available:

                raise forms.ValidationError(

                    "Doctor has not added available days"

                )


            # selected day unavailable

            if weekday not in available:

                raise forms.ValidationError(

                    f"Doctor unavailable on {weekday}"

                )


            # check start time

            if (

                self.doctor.available_from

                and

                t < self.doctor.available_from

            ):

                raise forms.ValidationError(

                    "Doctor unavailable at this time"

                )


            # check end time

            if (

                self.doctor.available_to

                and

                t > self.doctor.available_to

            ):

                raise forms.ValidationError(

                    "Doctor unavailable at this time"

                )


        return cleaned