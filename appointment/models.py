from django.db import models
from patient.models import Patient
from doctor.models import Doctor


class Appointment(models.Model):
 STATUS=(('pending','pending'),('approved','approved'),('rejected','rejected'),('completed','completed'))
 patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
 doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
 date=models.DateField()
 time=models.TimeField()
 reason=models.TextField()
 paid=models.BooleanField(default=False)
 amount=models.IntegerField(default=0)
 transaction=models.CharField(max_length=100,null=True,blank=True)
 status=models.CharField(max_length=20,choices=STATUS,default='pending')
 created=models.DateTimeField(auto_now_add=True)