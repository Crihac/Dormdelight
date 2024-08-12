from django.db import models

# Create your models here.
class Room(models.Model):
    FLOOR_CHOICES = [
        ("1", "First"),
        ("2", "Second"),
        ("3", "Third"),
        ("4", "Fourth"),
    ]
    TYPE_CHOICES = [
        ("1", "Single"),
        ("2", "Double"),
        ("3", "Triple"),
    ]
    room_number = models.CharField(max_length=3, primary_key=True, unique=True)
    floor = models.CharField(max_length=1, choices=FLOOR_CHOICES)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    ac = models.BooleanField(null=True, blank=True)
    rent = models.DecimalField(max_digits=7, decimal_places=2)
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_number}"

    @classmethod
    def get_unoccupied_rooms(cls):
        return cls.objects.filter(occupied=False)