from django import forms
from .models import User

class RegisterForm(forms.ModelForm):

 password=forms.CharField(
  widget=forms.PasswordInput
 )

 role=forms.ChoiceField(

  choices=[

   ('patient','patient'),

   ('doctor','doctor'),

   ('admin','admin')

  ]

 )

 class Meta:

  model=User

  fields=[

   'username',

   'email',

   'phone',

   'password',

   'role'

  ]