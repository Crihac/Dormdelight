from django.urls import path
from .views import (
    BookingListViewAdmin,
    CreateBookingView,
    UpdateBookingViewAdmin,
    UpdateVerificationiViewAdmin,
    BookingListView,
    VerificationListViewAdmin,
    BookingSuccessfulView,
)

app_name = "core"
urlpatterns = [
    path("create-booking/", CreateBookingView.as_view(), name="create-booking"),
    path(
        "booking-successful/",
        BookingSuccessfulView.as_view(),
        name="booking-successful",
    ),
    path(
        "update-verification/<str:resident_id>/",
        UpdateVerificationiViewAdmin.as_view(),
        name="update-verification-admin",
    ),
    path(
        "update-booking/<str:booking_id>/",
        UpdateBookingViewAdmin.as_view(),
        name="update-booking-admin",
    ),
    path("my-bookings/", BookingListView.as_view(), name="my-bookings"),
    path(
        "all-verifications/",
        VerificationListViewAdmin.as_view(),
        name="verification-list-admin",
    ),
    path(
        "all-bookings/",
        BookingListViewAdmin.as_view(),
        name="booking-list-admin",
    ),
]