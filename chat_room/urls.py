from django.urls import path
from chat_room.views import *

urlpatterns = [
    path(
        "chat/",
        ChatTemplateView.as_view(),
        name="chat"
    ),
    # API endpoints for chat functionality
    path('room/<int:room_id>/messages/', get_room_messages, name='get_messages'),
    path('room/<int:room_id>/send/', send_message, name='send_message'),
]

