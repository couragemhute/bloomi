from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from notification.helpers.global_email_sender import send_email_from_global_config

User = get_user_model()

@receiver(post_save, sender=User)
def notify_user_account_created(sender, instance, created, **kwargs):
    """
    Sends an email to the user when their account is successfully created.
    """
    if created:
        user = instance
        if user.email:
            email_subject = "Your account has been created"
            email_content = (
                f"Hello {user.full_name or user.email},\n\n"
                "Your account has been successfully created. "
                "You can now log in using your email and password.\n\n"
                "Thank you!"
            )
            recipient_email = user.email

            send_email_from_global_config(
                email_subject=email_subject,
                user=user.full_name or user.email,
                email_content=email_content,
                recipient_email=recipient_email,
                attachment=None
            )
