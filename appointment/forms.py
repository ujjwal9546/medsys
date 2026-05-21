from django import forms
from .models import Appointment
from datetime import date,datetime

class AppointmentForm(forms.ModelForm):

 class Meta:
  model=Appointment
  fields=['date','time','reason']

  widgets={
   'date':forms.DateInput(
    attrs={
     'type':'date',
     'min':date.today().isoformat()
    }
   ),

   'time':forms.TimeInput(
    attrs={'type':'time'}
   )
  }


 def clean(self):

  cleaned=super().clean()

  d=cleaned.get('date')

  t=cleaned.get('time')

  now=datetime.now()

  if d and d<date.today():

   raise forms.ValidationError(
   'Past date not allowed'
   )

  if d==date.today() and t:

   current=now.time()

   if t<current:

    raise forms.ValidationError(
    'Past time not allowed'
    )

  return cleaned