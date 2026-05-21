from django.db import models
from doctor.models import Doctor
from accounts.models import User


class Staff(models.Model):

 user=models.OneToOneField(User,on_delete=models.CASCADE)

 doctor=models.ForeignKey(
 Doctor,
 on_delete=models.CASCADE
 )

 designation=models.CharField(max_length=50)