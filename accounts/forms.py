from django import forms
from .models import User


class RegisterForm(forms.ModelForm):

    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Enter password'
            }
        )
    )


    confirm_password=forms.CharField(

        widget=forms.PasswordInput(

            attrs={
                'placeholder':
                'Confirm password'
            }

        )

    )


    role=forms.ChoiceField(

        choices=[

            ('patient','Patient'),

            ('doctor','Doctor')

        ]

    )


    class Meta:

        model=User

        fields=[

        'name',

        'username',

        'email',

        'phone',

        'password',

        'confirm_password',

        'role'

        ]

    def clean(self):

        cleaned_data=super().clean()

        password=cleaned_data.get(
            'password'
        )

        confirm=cleaned_data.get(
            'confirm_password'
        )


        if password!=confirm:

            raise forms.ValidationError(

                "Passwords do not match"

            )

        return cleaned_data
    

from django.contrib.auth.forms import UserCreationForm


class AddAdminForm(forms.ModelForm):

    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Password'
            }
        )
    )


    confirm_password=forms.CharField(

        widget=forms.PasswordInput(

            attrs={
                'placeholder':
                'Confirm password'
            }

        )

    )


    class Meta:

        model=User

        fields=[

        'name',

        'username',

        'email',

        'phone',

        'password',

        'confirm_password'

        ]

    def clean(self):

        cleaned=super().clean()

        p=cleaned.get(
            'password'
        )

        cp=cleaned.get(
            'confirm_password'
        )


        if p!=cp:

            raise forms.ValidationError(

                "Passwords do not match"

            )

        return cleaned