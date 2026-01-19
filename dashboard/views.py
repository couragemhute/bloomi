# views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
from role.mixins.role_permission_required import RolePermissionRequiredMixin

# class DashboardListView(LoginRequiredMixin,RolePermissionRequiredMixin,TemplateView):
#     template_name = 'dashboard/dashboard.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user

#         users = CustomUser.objects.all()
 
#         return context
    
#     def get_required_permissions(self):
#         return ["view_customuser"]

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .helpers import get_facilitator_dashboard_data


class DashboardListView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Global dashboard data
        context["user"] = user

        # FACILITATOR DATA
        if user.role and user.role.name == "Facillitator":
            context["facilitator"] = get_facilitator_dashboard_data(user)

        return context

    
    # def get_required_permissions(self):
    #     return ["view_customuser"]
