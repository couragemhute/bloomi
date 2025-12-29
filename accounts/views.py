from django.urls import reverse_lazy
from .models import CustomUser
from email.message import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from accounts.forms import CustomUserCreationForm, CustomUserUpdateForm
from accounts.models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_POST
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




class UserListView(LoginRequiredMixin,ListView):
    model = CustomUser
    template_name = 'registration/users/index.html'
    context_object_name = 'users'

class UserDetailView(LoginRequiredMixin,DetailView):
    model = CustomUser
    template_name = 'registration/users/details.html'
    context_object_name = 'users'   
    
class UserDeleteView(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        obj = get_object_or_404( CustomUser, pk=kwargs.get('pk'))
        obj.is_active = False
        obj.save()
        messages.success(request,f'{obj} deactivated successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
def register_user(request):
        if request.method == "GET":
            return render(
                request, "registration/users/create.html",
                {"form": CustomUserCreationForm}
            )
        elif request.method == "POST":
            form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("User created successfully"))
            return redirect('user-index')
        else:
            messages.success(request, ("Something went wrong please try again"))
            return redirect('user-create')
        
class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = CustomUser
    template_name = 'registration/users/update.html'
    form_class = CustomUserUpdateForm
    success_message = "User updated successfully"

    def get_success_url(self):
        return reverse("user-index")

    def form_valid(self, form):
        user = form.instance
        new_email = form.cleaned_data['email']

        if CustomUser.objects.exclude(pk=user.pk).filter(email=new_email).exists():
            form.add_error('email', 'A user with this email already exists.')
            return self.form_invalid(form)

        return super().form_valid(form)


    
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset-password')

        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            return redirect('account_login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('reset-password')
    else:
        return render(request, 'registration/users/reset.html')
    
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('account_login')


class EmployeeProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/users/profile.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'employee_profile'):
            context['employee'] = self.request.user.employee_profile
        context['password_form'] = PasswordChangeForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Prevent logout
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('user_profile')
        else:
            context = self.get_context_data()
            context['password_form'] = form
            return self.render_to_response(context)

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'account/password_reset_email.html'
    html_email_template_name = 'account/password_reset_email.html'

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        html_email = render_to_string(html_email_template_name, context)
        email_message = EmailMessage(
            subject_template_name,
            html_email,
            from_email,
            [to_email],
        )

        email_message.content_subtype = 'html'
        email_message.send()