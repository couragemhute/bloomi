
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
        name = request.POST.get("name")
        email = request.POST.get("email")
        priority = request.POST.get("priority")
        message = request.POST.get("message")

        logger.info("Received contact form submission from %s", email)

        try:
            user = "Website Visitor"
            recipient_email = "couragemhute21@gmail.com"

            email_subject = f"New Message from {name} - Priority: {priority}"
            email_content = (
                f"Message: {message}\n\n"
                f"Priority: {priority}\n\n"
                f"Visitor Email: {email}\n"
            )

            logger.debug("Email subject: %s", email_subject)
            logger.debug("Email content: %s", email_content)

            email_sent = send_email_from_global_config(email_subject, user, email_content, recipient_email)

            if email_sent:
                messages.success(request, "Your message has been sent successfully!")
                logger.info("Email sent successfully to %s", recipient_email)
            else:
                messages.error(request, "Failed to send the email. Please try again.")
                logger.error("Failed to send email to %s", recipient_email)

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            logger.exception("An error occurred while processing the contact form submission")

        return redirect("contact") 

    return render(request, "contact_form.html")