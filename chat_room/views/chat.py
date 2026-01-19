
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


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from chat_room.models import ChatRoom, ChatMessage, ChatParticipant
import json

@login_required
@require_http_methods(["GET"])
def get_room_messages(request, room_id):
    """Get all messages for a specific chat room"""
    try:
        # Check if user is a participant in this room
        room = ChatRoom.objects.get(id=room_id)
        if not ChatParticipant.objects.filter(room=room, user=request.user).exists():
            return JsonResponse({'error': 'You are not a participant in this room'}, status=403)
        
        # Get messages
        messages = ChatMessage.objects.filter(room=room).select_related('sender').order_by('created_at')
        
        messages_data = []
        for msg in messages:
            messages_data.append({
                'id': msg.id,
                'message': msg.message,
                'sender_name': msg.sender.full_name or msg.sender.email,
                "sender_image": msg.sender.image.url if msg.sender.image else "/static/images/default-user.png",
                'sender_id': msg.sender.id,
                'is_sent': msg.sender.id == request.user.id,
                'created_at': msg.created_at.isoformat(),
                'is_read': msg.is_read
            })
        
        return JsonResponse({
            'success': True,
            'messages': messages_data
        })
    
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Chat room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def send_message(request, room_id):
    """Send a message to a chat room"""
    try:
        # Check if user is a participant in this room
        room = ChatRoom.objects.get(id=room_id)
        if not ChatParticipant.objects.filter(room=room, user=request.user).exists():
            return JsonResponse({'error': 'You are not a participant in this room'}, status=403)
        
        # Parse request body
        data = json.loads(request.body)
        message_text = data.get('message', '').strip()
        
        if not message_text:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Create message
        message = ChatMessage.objects.create(
            room=room,
            sender=request.user,
            message=message_text
        )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'message': message.message,
                'sender_name': message.sender.get_full_name() or message.sender.username,
                'sender_id': message.sender.id,
                'is_sent': True,
                'created_at': message.created_at.isoformat()
            }
        })
    
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Chat room not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)