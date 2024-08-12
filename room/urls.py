from django.urls import path
from .views import AddRoomViewAdmin, RoomListView, RoomDetailView, UpdateRoomViewAdmin

app_name = "room"
urlpatterns = [
    path("floor/<str:floor>/", RoomListView.as_view(), name="room-list"),
    path(
        "floor/<str:floor>/room-add/", AddRoomViewAdmin.as_view(), name="room-add-admin"
    ),
    path(
        "floor/<str:floor>/<str:room_number>/",
        RoomDetailView.as_view(),
        name="room-detail",
    ),
    path(
        "floor/<str:floor>/<str:room_number>/room-update/",
        UpdateRoomViewAdmin.as_view(),
        name="room-update-admin",
    ),
]