from django.urls import path
from chat_room.views import *

urlpatterns = [
    path(
        "chat/",
        ChatTemplateView.as_view(),
        name="chat"
    ),
]
