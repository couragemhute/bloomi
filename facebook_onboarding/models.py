from django.db import models
from django.contrib.auth.models import User

class OnboardedClient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    business_name = models.CharField(max_length=255)
    whatsapp_business_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # waba_id
    business_id = models.CharField(max_length=255, null=True, blank=True)  # portfolio id
    phone_number_id = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)          # short-lived token (optional)
    long_lived_token = models.TextField(null=True, blank=True)     # long-lived business token
    onboarded_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    meta = models.JSONField(null=True, blank=True)  # store raw FB responses for audit
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.business_name} ({self.whatsapp_business_id})"
