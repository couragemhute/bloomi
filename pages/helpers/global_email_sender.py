
from django.core.mail import EmailMultiAlternatives
# from core.settings import DEFAULT_FROM_EMAIL
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
import logging


def send_email_from_global_config(email_subject, user, email_content, recipient_email):
    email_html_content = render_to_string(
        "notification/emails/global_email.html",
        {"username": user, "your_email_content": email_content, "recipient_email": recipient_email},
    )

    email_message = EmailMultiAlternatives(
        email_subject,
        email_html_content,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],  
    )
    email_message.content_subtype = "html"  

    try:
        email_message.send()
        print(f"Email sent to {recipient_email}")
        return True
    except Exception as e:
        error_message = f"Failed to send email to {recipient_email}: {str(e)}"
        print(error_message)
        return False
    
logger = logging.getLogger(__name__)

def contact_form_submission(request):
    if request.method == "POST":
        name = request.POST.get("fname", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "No Subject").strip()
        message = request.POST.get("msg", "").strip()

        logger.info(f"Contact form submitted by {email}")

        try:
            user = "Website Visitor"
            recipient_emails = [
                "courage@ultimatecreative.co.zw",
            ]

            email_sent_all = True
            for recipient in recipient_emails:
                email_subject = f"New Message from {name} - Subject: {subject}"
                email_content = (
                    f"Message:\n{message}\n\n"
                    f"From:\nName: {name}\nEmail: {email}\n"
                )
                logger.debug(f"Sending email to {recipient} with subject: {email_subject}")
                sent = send_email_from_global_config(email_subject, user, email_content, recipient)
                if sent:
                    logger.info(f"Email sent to {recipient}")
                else:
                    email_sent_all = False
                    logger.error(f"Failed to send email to {recipient}")

            if email_sent_all:
                messages.success(request, "Your message has been sent successfully!")
            else:
                messages.error(request, "Some emails failed to send. Please try again later.")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            logger.exception("Exception during contact form email sending")

        return redirect("contact")

    return render(request, "pages/contact/index.html")