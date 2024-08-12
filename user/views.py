from django.shortcuts import redirect, render, reverse
from django.views.generic import ListView, View, CreateView, UpdateView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AdminUserTestMixin
from django.urls import reverse_lazy

from .forms import ResidentUpdateFormAdmin, UserRegisterForm, ResidentUpdateForm
from .models import User, Resident

from core.models import Booking, Verification

# Create your views here.
class CreateUserView(CreateView):
    template_name = "user/register.html"
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("user:user-login")


class ResidentDetailView(LoginRequiredMixin, DetailView):
    model = Resident
    slug_url_kwarg = "resident_id"
    slug_field = "resident_id"


class ResidentUpdateView(LoginRequiredMixin, UpdateView):
    model = Resident
    form_class = ResidentUpdateForm
    template_name = "user/resident_update.html"
    slug_field = "resident_id"
    slug_url_kwarg = "resident_id"

    def get_success_url(self):
        return reverse(
            "user:user-detail", args=[self.request.user.resident.resident_id]
        )


class DashboardViewAdmin(LoginRequiredMixin, AdminUserTestMixin, View):
    template_name = "user/admin/admin_dashboard.html"

    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.all()
        pending_bookings = bookings.filter(status="0").order_by("date_applied")
        complete_bookings = bookings.filter(status="1").order_by("date_applied")

        verifications = Verification.objects.all()
        pending_verifications = verifications.filter(status="0")
        complete_verifications = verifications.filter(status="1")
        context = {
            "pending_bookings": pending_bookings,
            "complete_bookings": complete_bookings,
            "pending_verifications": pending_verifications,
            "complete_verifications": complete_verifications,
        }
        return render(request, self.template_name, context)


class ResidentListViewAdmin(LoginRequiredMixin, AdminUserTestMixin, ListView):
    model = Resident
    template_name = "user/admin/resident_list_admin.html"

    def get_queryset(self):
        residents = super().get_queryset()
        return residents.filter(user__is_admin=False)


class ResidentUpdateViewAdmin(LoginRequiredMixin, AdminUserTestMixin, UpdateView):
    model = Resident
    form_class = ResidentUpdateFormAdmin
    template_name = "user/admin/resident_update_admin.html"
    success_url = reverse_lazy("user:user-list-admin")
    slug_field = "resident_id"
    slug_url_kwarg = "resident_id"