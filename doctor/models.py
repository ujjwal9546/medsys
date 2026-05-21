from django.db import models
from accounts.models import User

class Doctor(models.Model):

 user=models.OneToOneField(
 User,
 on_delete=models.CASCADE
 )

 photo=models.ImageField(
 upload_to='doctor/',
 null=True,
 blank=True
 )

 specialization=models.CharField(
 max_length=100
 )

 qualification=models.CharField(
 max_length=200
 )

 experience=models.IntegerField()

 hospital=models.CharField(
 max_length=200
 )

 fee=models.IntegerField()

 bio=models.TextField(
 null=True,
 blank=True
 )

 location=models.CharField(
 max_length=200,
 null=True,
 blank=True
 )

 phone=models.CharField(
 max_length=15,
 null=True
 )

 available_from=models.TimeField(
 null=True
 )

 available_to=models.TimeField(
 null=True
 )

 def __str__(self):
  return self.user.username