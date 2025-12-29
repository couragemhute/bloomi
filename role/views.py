from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    TemplateView,
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from role.forms import RoleForm
from django.urls import reverse_lazy
from role.mixins.role_permission_required import RolePermissionRequiredMixin
from .models import Role
from django.contrib.auth.models import Permission
from django.http import HttpResponseRedirect
from django.views import View
from accounts.models import CustomUser
from django.contrib.auth.models import Permission


class PermissionListView(LoginRequiredMixin,RolePermissionRequiredMixin, ListView):
    model = Permission
    context_object_name = "permissions"
    template_name = "registration/permission/list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_required_permissions(self):
        return ['view_permission']
    
class RoleListView(LoginRequiredMixin, RolePermissionRequiredMixin, ListView):
    model = Role
    context_object_name = "roles"
    template_name = "registration/role/list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_required_permissions(self):
        return ['view_role']


class RoleCreateView(LoginRequiredMixin, SuccessMessageMixin, RolePermissionRequiredMixin, CreateView):
    model = Role
    form_class = RoleForm
    template_name = "registration/role/create.html"
    success_message = "Role created successfully"

    def get_success_url(self):
        return reverse("role-list")
    
    def get_required_permissions(self):
        return ['add_role']


class RoleDetailsView(LoginRequiredMixin, RolePermissionRequiredMixin, DetailView):
    model = Role
    context_object_name = "role"
    template_name = "registration/role/details.html"
    
    def get_required_permissions(self):
        return ['view_role']


class RoleUpdateView(LoginRequiredMixin, RolePermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Role
    context_object_name = "Role"
    template_name = "registration/role/update.html"
    form_class = RoleForm
    success_message = "Role updated successfully"

    def get_success_url(self):
        return reverse("role-list")
    
    def get_required_permissions(self):
        return ['change_role']

class RoleDeleteView(LoginRequiredMixin, SuccessMessageMixin, RolePermissionRequiredMixin, DeleteView):
    model = Role
    success_url = reverse_lazy("role-list")
    
    
    def dispatch(self, request, *args, **kwargs):
        # Check if the role being deleted is associated with a CustomUser
        role = self.get_object()
        if CustomUser.objects.filter(role=role).exists():
            messages.warning(self.request, "You cannot delete a role that is associated with a user.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return super().dispatch(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"{self.object.name} deleted successfully"
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

    def get_required_permissions(self):
        return ['delete_role']


class RemoveRolePermissionDeleteView(RolePermissionRequiredMixin, View):
    def get(self, request, role_pk, **kwargs):
        permission = get_object_or_404(Permission, pk=kwargs.get('pk'))
        role = get_object_or_404(Role, pk=role_pk)
        role.permissions.remove(permission)
        messages.success(request, f"'{permission.name}' permission removed from the role.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def post(self, request, role_pk, **kwargs):
        # Handling POST request here
        permission = get_object_or_404(Permission, pk=kwargs.get('pk'))
        role = get_object_or_404(Role, pk=role_pk)
        role.permissions.remove(permission)
        messages.success(request, f"'{permission.name}' permission removed from the role.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_required_permissions(self):
        return ['delete_role']