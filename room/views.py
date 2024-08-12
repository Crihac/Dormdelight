from django.shortcuts import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from user.mixins import AdminUserTestMixin

from .models import Room

# Create your views here.
class RoomListView(ListView):
    model = Room

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["room_list"] = (
            context["room_list"]
            .filter(floor=self.kwargs.get("floor"))
            .order_by("occupied")
        )
        context["floor"] = self.kwargs.get("floor")
        return context


class RoomDetailView(DetailView):
    model = Room
    pk_url_kwarg = "room_number"


class AddRoomViewAdmin(LoginRequiredMixin, AdminUserTestMixin, CreateView):
    model = Room
    fields = ["room_number", "type", "ac", "rent", "occupied"]
    template_name = "room/admin/room_form_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["floor"] = self.kwargs.get("floor")
        return context

    def form_valid(self, form):
        form.instance.floor = self.kwargs.get("floor")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "room:room-detail", args=[self.object.floor, self.object.room_number]
        )


class UpdateRoomViewAdmin(LoginRequiredMixin, AdminUserTestMixin, UpdateView):
    model = Room
    fields = ["type", "ac", "rent", "occupied"]
    template_name = "room/admin/room_form_admin.html"
    pk_url_kwarg = "room_number"

    def get_success_url(self):
        return reverse(
            "room:room-detail", args=[self.object.floor, self.object.room_number]
        )