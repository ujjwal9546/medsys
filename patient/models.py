from django.db import models
from accounts.models import User

class Patient(models.Model):

 user=models.OneToOneField(User,on_delete=models.CASCADE)

 age=models.IntegerField()

 gender=models.CharField(max_length=20)