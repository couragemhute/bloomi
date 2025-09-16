from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import CustomUser
from .forms import CustomUserForm


# ---------- CustomUser Views ----------
class UserListView(ListView):
    model = CustomUser
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"
    context_object_name = "user"


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")


class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")


