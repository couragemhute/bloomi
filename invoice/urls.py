from django.urls import path

from pages.helpers.global_email_sender import contact_form_submission
from .views import InvoiceTemplateView, create_invoice

urlpatterns = [
    path('invoice/', InvoiceTemplateView.as_view(), name='invoice'),
    path('invoice/create/', create_invoice, name='create_invoice'),
]
