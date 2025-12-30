# views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
from role.mixins.role_permission_required import RolePermissionRequiredMixin

class DashboardListView(LoginRequiredMixin,RolePermissionRequiredMixin,TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        users = CustomUser.objects.all()
 
        return context
    
    def get_required_permissions(self):
        return ["view_customuser"]

