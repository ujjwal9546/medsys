from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

 ROLE=(
 ('patient','patient'),
 ('doctor','doctor'),
 ('admin','admin'),
 ('staff','staff')
 )

 role=models.CharField(max_length=20,choices=ROLE,default='patient')
 approved=models.BooleanField(default=False)
 phone=models.CharField(max_length=15)