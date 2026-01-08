from django.urls import reverse_lazy
from .models import CustomUser, Profession, Qualification
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
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser, FacilitatorProfile
from .forms import FacilitatorProfileForm


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

class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'registration/users/details.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['professions'] = Profession.objects.all()
        context['qualifications'] = Qualification.objects.all()
        context['user'] = self.request.user
        return context
 
    
class UserDeleteView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs.get('pk'))

        # Toggle active status
        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])

        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"{user} {status} successfully")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

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


# --- Facilitator Profile Update (existing) ---
class FacilitatorProfileUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs.get('pk'))
        profile, created = FacilitatorProfile.objects.get_or_create(user=user)
        form = FacilitatorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"Facilitator profile for {user.full_name} updated successfully.")
        else:
            messages.error(request, f"Error updating profile: {form.errors}")
        return redirect(request.META.get('HTTP_REFERER', '/'))

# --- Add Profession ---
@require_POST
def profession_add(request):
    name = request.POST.get('name')
    user = request.user

    if not name:
        messages.error(request, "Profession name cannot be empty.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Check if the user already has a profession
    profession, created = Profession.objects.get_or_create(user=user)
    profession.name = name
    profession.save()

    if created:
        messages.success(request, "Profession added successfully.")
    else:
        messages.success(request, "Profession updated successfully.")

    return redirect(request.META.get('HTTP_REFERER', '/'))

# --- Add Qualification ---
@require_POST
def qualification_add(request):
    name = request.POST.get('name')
    institution = request.POST.get('institution', '')
    year_obtained = request.POST.get('year_obtained')
    certificate = request.FILES.get('certificate')
    user = request.user

    if name:
        Qualification.objects.create(
            user=user,
            name=name,
            institution=institution,
            year_obtained=year_obtained if year_obtained else None,
            certificate=certificate
        )
        messages.success(request, "Qualification added successfully.")
    else:
        messages.error(request, "Qualification name cannot be empty.")

    return redirect(request.META.get('HTTP_REFERER', '/'))


