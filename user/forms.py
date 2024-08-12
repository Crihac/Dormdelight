from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Resident


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]


class ResidentUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    def __init__(self, *args, **kwargs):
        super(ResidentUpdateForm, self).__init__(*args, **kwargs)
        user = kwargs.get("instance").user
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name

    class Meta:
        model = Resident
        fields = [
            "first_name",
            "last_name",
            "father_name",
            "address",
            "profession",
            "work_address",
        ]

    def save(self, commit=True, *args, **kwargs):
        instance = super(ResidentUpdateForm, self).save(commit)
        user = instance.user
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.save()
        return instance


class ResidentUpdateFormAdmin(forms.ModelForm):
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = Resident
        fields = ["room", "check_in_date", "is_admin"]

    def save(self, commit=True):
        instance = super().save(commit)
        user = instance.user
        user.is_admin = self.cleaned_data.get("is_admin")
        user.save()
        return instance