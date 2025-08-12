# videos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_ai_video, name='generate_ai_video'),
]
