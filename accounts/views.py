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


from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from .forms import UserRegistrationForm

class RegisterUserView(View):
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return redirect(request.META.get('HTTP_REFERER'))


# users/views.py
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_POST

@require_POST
def login_modal(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)
    referer = request.META.get('HTTP_REFERER', '/')

    if user is not None:
        login(request, user)
        messages.success(request, "Successfully logged in!")
        return redirect(referer)
    else:
        messages.error(request, "Invalid email or password!")
        return redirect(referer)
