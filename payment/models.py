from django.db import models
import uuid

from user.models import Resident
from room.models import Room

# Create your models here.
class Payment(models.Model):
    STATUS_CHOICE = [
        ("0", "FAILURE"),
        ("1", "SUCCESS"),
        ("2", "PENDING"),
    ]
    payment_id = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid.uuid4
    )
    payer = models.ForeignKey(
        Resident, null=True, blank=True, on_delete=models.SET_NULL
    )
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default="2")
    date_of_payment = models.DateTimeField(null=True, blank=True)

    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.payer} -> ({self.room},{self.status})"