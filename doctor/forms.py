from django.forms import ModelForm
from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):

 class Meta:

  model=Doctor

  exclude=['user']


 def clean_fee(self):

  fee=self.cleaned_data['fee']

  if fee<=0:

   raise forms.ValidationError(

    "Fee must be greater than 0"

   )

  return fee