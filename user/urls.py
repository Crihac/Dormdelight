from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    CreateUserView,
    ResidentListViewAdmin,
    ResidentUpdateView,
    ResidentDetailView,
    DashboardViewAdmin,
    ResidentUpdateViewAdmin,
)

from core.views import CreateResidentVerificationView

app_name = "user"
urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-register"),
    path(
        "login/", LoginView.as_view(template_name="user/login.html"), name="user-login"
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="user/logout.html"),
        name="user-logout",
    ),
    path("update/<slug:resident_id>", ResidentUpdateView.as_view(), name="user-update"),
    path(
        "verification/",
        CreateResidentVerificationView.as_view(),
        name="user-verification",
    ),
    # paths for admin user
    path("admin/dashboard/", DashboardViewAdmin.as_view(), name="admin-dashboard"),
    path("admin/all-users/", ResidentListViewAdmin.as_view(), name="user-list-admin"),
    path(
        "admin/update/<slug:resident_id>/",
        ResidentUpdateViewAdmin.as_view(),
        name="user-update-admin",
    ),
    ########################
    path("<int:resident_id>/", ResidentDetailView.as_view(), name="user-detail"),
]