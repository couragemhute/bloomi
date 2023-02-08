from django.urls import path
from home.views import HomeListView

urlpatterns = [
    path('', HomeListView.as_view(), name="home")
]
