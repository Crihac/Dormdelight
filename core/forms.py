from django import forms
from .models import Verification


class ResidentVerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = ["id_type", "id_number"]