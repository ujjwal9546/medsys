from django.db import models
from patient.models import Patient
from doctor.models import Doctor


class Appointment(models.Model):

    STATUS=(

        ('pending','pending'),
        ('approved','approved'),
        ('rejected','rejected'),
        ('completed','completed')

    )


    PAYMENT_STATUS=(

        ('unpaid','unpaid'),
        ('submitted','submitted'),
        ('verified','verified'),
        ('rejected','rejected')

    )


    patient=models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )


    doctor=models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )


    date=models.DateField()

    time=models.TimeField()

    reason=models.TextField()


    amount=models.IntegerField(
        default=0
    )


    coupon_code=models.CharField(

        max_length=50,

        blank=True,

        null=True

    )


    discount=models.IntegerField(

        default=0

    )


    final_amount=models.IntegerField(

        default=0

    )


    status=models.CharField(

        max_length=20,

        choices=STATUS,

        default='pending'

    )


    payment_status=models.CharField(

        max_length=20,

        choices=PAYMENT_STATUS,

        default='unpaid'

    )


    payment_screenshot=models.ImageField(

        upload_to='payments/',

        null=True,

        blank=True

    )


    created=models.DateTimeField(
        auto_now_add=True
    )


    hidden_by_patient=models.BooleanField(
        default=False
    )


    hidden_by_doctor=models.BooleanField(
        default=False
    )


    def __str__(self):

        return f"{self.patient} - {self.doctor}"