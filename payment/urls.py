from django.urls import path
from .views import (
    request_payment,
    handle_payment,
    PaymentListViewAdmin,
    PaymentDetailViewAdmin,
)

app_name = "payment"
urlpatterns = [
    path("request-payment/", request_payment, name="request-payment"),
    path("handle-payment/", handle_payment, name="handle-payment"),
    path("all-payments/", PaymentListViewAdmin.as_view(), name="payment-list-admin"),
    path(
        "<slug:payment_id>/",
        PaymentDetailViewAdmin.as_view(),
        name="payment-detail-admin",
    ),
]