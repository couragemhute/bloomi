
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.views.generic import TemplateView
from chat_room.models import ChatRoom, ChatParticipant
from django.contrib.auth.mixins import LoginRequiredMixin

class ChatTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "chat/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # General (group) chat rooms
        context['general_rooms'] = ChatRoom.objects.filter(room_type="Group").order_by("-created_at")

        # Private chat rooms where user participates
        context['personal_rooms'] = ChatParticipant.objects.filter(user=user, room__room_type="Private").select_related('room', 'user')

        # All group chat rooms the user is a participant in (could be same as general if needed)
        context['group_rooms'] = ChatParticipant.objects.filter(user=user, room__room_type="Group").select_related('room', 'user')

        return context
