from django.db import models
from accounts.models import User

class Notification(models.Model):

 user=models.ForeignKey(
 User,
 on_delete=models.CASCADE
 )

 msg=models.TextField()

 seen=models.BooleanField(
 default=False
 )