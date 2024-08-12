# from django.core.exceptions import ValidationError
from django.db import models
from user.models import Resident
from room.models import Room
from django.utils import timezone
import uuid

# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = [
        ("0", "In Process"),
        ("1", "Confirmed"),
        ("2", "Canceled"),
    ]
    id = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid.uuid4
    )
    applicant = models.ForeignKey(Resident, null=True, on_delete=models.SET_NULL)
    date_applied = models.DateTimeField(auto_now_add=True)
    room_applied = models.CharField(max_length=3, default="xxx")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="0")

    def __str__(self):
        return f"{self.applicant} -> {self.room_applied}"

    # def clean(self):
    #     old_bookings = Booking.objects.filter(
    #         applicant=self.applicant, status="0"
    #     ).exclude(id=self.id)
    #     if old_bookings.exists():
    #         raise ValidationError(
    #             {"status": "A Booking is already pending for this applicant."}
    #         )
    #     verification = Verification.objects.filter(person=self.applicant)
    #     if not verification.exists():
    #         raise ValidationError(
    #             {"applicant": "Applicant must be verified before booking a room."}
    #         )

    #     current_room = Room.objects.filter(room_number=self.room_applied)
    #     if not current_room:
    #         raise ValidationError(
    #             {"room_applied": "Room with given room number does not exists"}
    #         )

    def save(self, *args, **kwargs):
        if self.status == "1":
            current_room = Room.objects.filter(room_number=self.room_applied)
            self.applicant.room = current_room[0]
            self.applicant.check_in_date = timezone.localtime(timezone.now())
            self.applicant.save()
        return super(Booking, self).save(*args, **kwargs)


class Verification(models.Model):
    ID_CHOICES = [
        ("1", "Institutional ID"),
        ("2", "Aadhar Number"),
        ("3", "Voter ID"),
        ("4", "Driving License"),
        ("5", "Passport"),
    ]
    STATUS_CHOICES = [
        ("0", "In Process"),
        ("1", "Verified"),
        ("2", "Canceled"),
    ]
    person = models.OneToOneField(
        Resident,
        primary_key=True,
        to_field="resident_id",
        serialize=False,
        on_delete=models.CASCADE,
    )
    id_type = models.CharField(max_length=1, choices=ID_CHOICES)
    id_number = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="0")

    class Meta:
        unique_together = ["id_type", "id_number"]

    def __str__(self):
        return f"{self.person}"