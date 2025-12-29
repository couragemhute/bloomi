import mimetypes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_email_from_global_config(email_subject, user, email_content, recipient_email, attachment=None, attachment_name=None):
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

    if attachment:
        # Use the provided attachment_name if available, else fallback to attachment.name
        filename_to_use = attachment_name if attachment_name else getattr(attachment, 'name', 'attachment')
        # Get the content type for the file using mimetypes
        content_type, _ = mimetypes.guess_type(filename_to_use)
        # Attach the file with the correct content type and the chosen filename
        email_message.attach(filename_to_use, attachment.read(), content_type or 'application/octet-stream')

    try:
        # print(f"Email Subject: {email_subject}")
        # print(f"User: {user}")
        # print(f"Email Content: {email_content}")
        # print(f"Recipient Email: {recipient_email}")
        # print(f"Attachment: {filename_to_use if attachment else None}")

        email_message.send()
        print(f"Email sent to {recipient_email}")
        return True
    except Exception as e:
        error_message = f"Failed to send email to {recipient_email}: {str(e)}"
        print(error_message)
        return False
