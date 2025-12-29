from django.urls import path

from dashboard.views import DashboardListView

urlpatterns = [
    path('home/', DashboardListView.as_view(), name="dashboard"),   
]
