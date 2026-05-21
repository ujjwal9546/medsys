from django.db import models
from appointment.models import Appointment

class Payment(models.Model):

 appointment=models.OneToOneField(
 Appointment,
 on_delete=models.CASCADE
 )

 amount=models.IntegerField()

 transaction=models.CharField(
 max_length=100
 )

 success=models.BooleanField(
 default=False
 )