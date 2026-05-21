from django import forms
from accounts.models import User
class StaffForm(forms.ModelForm):
 password=forms.CharField(widget=forms.PasswordInput)
 class Meta:model=User;fields=['username','email','phone','password']