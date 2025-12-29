# notifications/utils.py

from django.contrib.contenttypes.models import ContentType
from notification.models import Notification


def create_notification(user, obj, title, message):
    content_type = ContentType.objects.get_for_model(obj.__class__)
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        content_type=content_type,
        object_id=obj.id,
    )
