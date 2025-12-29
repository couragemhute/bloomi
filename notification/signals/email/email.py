# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from notification.helpers.global_email_sender import send_email_from_global_config
from notification.models import Notification

User = get_user_model()

@receiver(post_save, sender=Notification)
def notify_user_on_new_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if user and user.email:
            email_subject = instance.title
            email_content = instance.message
            recipient_email = user.email

            send_email_from_global_config(
                email_subject=email_subject,
                user=user.get_full_name() or user.username,
                email_content=email_content,
                recipient_email=recipient_email,
                attachment=None  # or add instance.attachment if you store files
            )
    