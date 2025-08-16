# bot/urls.py
from django.urls import path
from .views import exchange_fb_code

urlpatterns = [
    path("exchange-code/", exchange_fb_code, name="exchange_fb_code"),
]
