from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect

class RolePermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        required_permissions = self.get_required_permissions()

        if request.user.is_anonymous:
            messages.warning(request, "You must be logged in.")
            return redirect('login')

        # ✅ Superuser bypasses all checks
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not request.user.role:
            messages.warning(request, "You don't have a role assigned.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        user_permissions = request.user.role.permissions.values_list('codename', flat=True)

        if not any(perm in user_permissions for perm in required_permissions):
            messages.warning(request, f"You don't have permission to view this page. Required: {', '.join(required_permissions)}")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        return super().dispatch(request, *args, **kwargs)

    def get_required_permissions(self):
        raise NotImplementedError("Subclasses must define get_required_permissions")
