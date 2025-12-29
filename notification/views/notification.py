# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from notification.models import Notification
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = "notifications"
    template_name = "notification/user_notifications/list.html"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
@login_required
def fetch_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    data = []
    for n in notifications:
        data.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%b %d, %I:%M %p')
        })
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'notifications': data, 'unread_count': unread_count})

@require_POST
@login_required
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.mark_as_read()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
