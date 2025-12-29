from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from helpers.timestamp import TimestampMixin

class Notification(TimestampMixin):
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)

    # Optionally notify a specific user, or null for global notification
    user = models.ForeignKey('accounts.CustomUser', null=True, blank=True, on_delete=models.CASCADE, related_name='notifications')

    # Optional generic relation to any object
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title


class NotificationReadStatus(TimestampMixin):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('notification', 'user')
