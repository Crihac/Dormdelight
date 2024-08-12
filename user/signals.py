from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Resident


@receiver(post_save, sender=User)
def create_resident(sender, instance, created, **kwargs):
    print("creating resident")
    if created:
        Resident.objects.create(user=instance)