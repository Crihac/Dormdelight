from django.shortcuts import redirect
from django.http import JsonResponse

from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, View, CreateView, ListView, TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from user.mixins import AdminUserTestMixin

from http import HTTPStatus
import json

from .models import Booking, Verification
from .forms import ResidentVerificationForm
from room.models import Room
from payment.models import Payment

# Create your views here.
class CreateBookingView(View):
    def post(self, request, *args, **kwargs):
        context = {
            "success": True,
            "redirect": False,
            "message": "Booking successful, please wait till it is confirmed...",
        }
        if not request.user.is_authenticated:
            context["success"] = False
            context["redirect"] = True
            context["redirect_url"] = reverse("user:user-login")
            context["message"] = "Login to make a booking"
            return JsonResponse(context, status=HTTPStatus.TEMPORARY_REDIRECT)

        room_number = json.load(request).get("room_number")
        room = Room.objects.filter(room_number=room_number)
        if not room:
            context["success"] = False
            context["message"] = "Room with given room number does not exists"
            return JsonResponse(context, status=HTTPStatus.BAD_REQUEST)

        # checking if room is already occupied
        if room[0].occupied:
            context["success"] = False
            context["message"] = "Room is not vaccant"
            return JsonResponse(context, status=HTTPStatus.BAD_REQUEST)

        # if not resident verified stuff :
        if not Verification.objects.filter(person=request.user.resident):
            context["success"] = False
            context["redirect"] = True
            context["redirect_url"] = reverse("user:user-verification")
            context["message"] = "Applicant not verified"
            return JsonResponse(context, status=HTTPStatus.TEMPORARY_REDIRECT)

        # checking for old pending bookings
        old_bookings = Booking.objects.filter(applicant=request.user.resident).filter(
            status="0"
        )
        if old_bookings:
            context["success"] = False
            context["message"] = "Pending booking exists already"
            return JsonResponse(context, status=HTTPStatus.BAD_REQUEST)

        # checking if payment done or not
        payment = Payment.objects.filter(payer=request.user.resident).filter(
            room=room[0]
        )
        if not payment:
            context["success"] = False
            context["redirect"] = True
            context["redirect_url"] = reverse("payment:request-payment")
            context["message"] = "Make payment first"

            request.session["resident_id"] = request.user.resident.resident_id
            request.session["room_number"] = room_number
            return JsonResponse(context, status=HTTPStatus.TEMPORARY_REDIRECT)

        # finally create the booking
        booking = Booking.objects.create(
            applicant=request.user.resident, room_applied=room_number
        )
        return JsonResponse(context, status=HTTPStatus.OK)


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking

    def get_queryset(self):
        bookings = super().get_queryset()
        return bookings.filter(applicant=self.request.user.resident).order_by(
            "-date_applied"
        )


class CreateResidentVerificationView(LoginRequiredMixin, CreateView):
    model = Verification
    form_class = ResidentVerificationForm
    template_name = "core/resident_verification_form.html"

    def form_valid(self, form):
        form.instance.person = self.request.user.resident
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "user:user-detail",
            kwargs={"resident_id": self.request.user.resident.resident_id},
        )


############################################################################################
class UpdateVerificationiViewAdmin(LoginRequiredMixin, AdminUserTestMixin, UpdateView):
    fields = ["status"]
    model = Verification
    pk_url_kwarg = "resident_id"
    template_name = "core/admin/update_verification_admin.html"
    success_url = reverse_lazy("core:verification-list-admin")


class UpdateBookingViewAdmin(LoginRequiredMixin, AdminUserTestMixin, UpdateView):
    fields = ["room_applied", "status"]
    model = Booking
    pk_url_kwarg = "booking_id"
    template_name = "core/admin/update_booking_admin.html"
    success_url = reverse_lazy("core:booking-list-admin")

    def form_valid(self, form):
        booking = self.object
        verification = Verification.objects.filter(person=booking.applicant)
        if not verification.exists() or verification[0].status == "0":
            form.add_error(None, "Resident not verified")
            return self.form_invalid(form)

        current_room = Room.objects.filter(room_number=booking.room_applied)
        if not current_room:
            form.add_error(
                "room_applied", "Room with given room number does not exists"
            )
            return self.form_invalid(form)

        return super().form_valid(form)


class VerificationListViewAdmin(LoginRequiredMixin, AdminUserTestMixin, ListView):
    model = Verification
    template_name = "core/admin/verification_list_admin.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        all_verifications = super().get_context_data(object_list=object_list, **kwargs)
        context = {
            "pending_verifications": all_verifications["object_list"].filter(
                status="0"
            ),
            "successful_verifications": all_verifications["object_list"].filter(
                status="1"
            ),
            "cancled_verifications": all_verifications["object_list"].filter(
                status="2"
            ),
        }
        return context


class BookingListViewAdmin(LoginRequiredMixin, AdminUserTestMixin, ListView):
    model = Booking
    template_name = "core/admin/booking_list_admin.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        all_bookings = super().get_context_data(object_list=object_list, **kwargs)
        context = {
            "pending_bookings": all_bookings["object_list"].filter(status="0"),
            "successful_bookings": all_bookings["object_list"].filter(status="1"),
            "cancled_bookings": all_bookings["object_list"].filter(status="2"),
        }
        return context


class BookingSuccessfulView(TemplateView):
    template_name = "core/booking_successful.html"