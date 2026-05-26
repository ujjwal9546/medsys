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

 SPECIALIZATION=(

 ('Cardiology','Cardiology'),

 ('Neurology','Neurology'),

 ('Orthopedic','Orthopedic'),

 ('Dermatology','Dermatology'),

 ('Pediatric','Pediatric'),

 ('ENT','ENT'),

 ('Psychiatry','Psychiatry'),

 ('Gynecology','Gynecology'),

 ('General','General'),

 ('Other','Other')

 )


 specialization=models.CharField(

 max_length=100,

 choices=SPECIALIZATION,

 default='General'
 
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

 DAY_CHOICES = [

 ('Mon','Monday'),
 ('Tue','Tuesday'), 
 ('Wed','Wednesday'),
 ('Thu','Thursday'),
 ('Fri','Friday'),
 ('Sat','Saturday'),
 ('Sun','Sunday'),

 ]


 available_days=models.CharField(

 max_length=100,

 blank=True,

 null=True,

 help_text="Select available days"

 )

 payment_qr=models.ImageField(
 upload_to='doctor_qr/',
 null=True,
 blank=True
 )

 def __str__(self):
   return (

 self.user.name

 if self.user.name

 else

 self.user.username

 )
  