from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
import logging
from blog.models import Blog, Subscriber
from pages.helpers.global_email_sender import send_email_from_global_config
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Blog)
def send_blog_notification(sender, instance, created, **kwargs):
    if created:  # Only on new blog creation
        subscribers = Subscriber.objects.all()
        subject = f"New Blog Published: {instance.title}"
        email_content = instance.content[:200] + "..."  # short preview
        user = "Blog Admin"

        for sub in subscribers:
            try:
                sent = send_email_from_global_config(
                    subject,
                    user,
                    email_content,
                    sub.email,
                )
                if sent:
                    logger.info(f"Blog email sent to {sub.email}")
                else:
                    logger.error(f"Failed to send blog email to {sub.email}")
            except Exception as e:
                logger.exception(f"Error sending blog email to {sub.email}: {e}")
