from django.contrib import admin
from .models import User, Resident

from room.models import Room
from django import forms

admin.site.register(User)

# custom form for showing currently allocated & available rooms only
class ResidentAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        resident = kwargs.get("instance")
        if resident and resident.room:
            # Include the currently assigned room in the queryset
            self.fields["room"].queryset = (
                Room.objects.filter(pk=resident.room.pk) | Room.get_unoccupied_rooms()
            )
        else:
            self.fields["room"].queryset = Room.get_unoccupied_rooms()


class ResidentAdmin(admin.ModelAdmin):
    form = ResidentAdminForm


admin.site.register(Resident, ResidentAdmin)