from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager
from room.models import Room 
from .utils import generate_resident_id

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class Resident(models.Model):
    resident_id = models.SlugField(unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)
    work_address = models.CharField(max_length=100, null=True, blank=True)
    room = models.OneToOneField(Room, null=True, blank=True, on_delete=models.SET_NULL)
    check_in_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # first clearing the status of room in the database
        q = Resident.objects.filter(pk=self.pk)
        if q and q[0].room:
            q[0].room.occupied = False
            q[0].room.save()
        # setting occupied for correct room
        if self.room:
            self.room.occupied = True
            self.room.save()

        if not self.resident_id:
            resident_ids = get_all_resident_ids()
            self.resident_id = generate_resident_id(self.user.first_name, resident_ids)

        super(Resident, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.resident_id}"


def get_all_resident_ids():
    residents = Resident.objects.all()
    resident_ids = set()
    for r in residents:
        if r.resident_id:
            resident_ids.add(r.resident_id)

    return resident_ids