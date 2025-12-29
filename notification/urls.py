# urls.py
from django.urls import path

from notification.views.notification import fetch_notifications, mark_notification_read, NotificationListView


urlpatterns = [
    path('notifications/', fetch_notifications, name='fetch_notifications'),
    path('notifications/read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path('notifications/list/', NotificationListView.as_view(), name='notification_list'),
]
