
from django.db import models
from django.contrib.auth.models import User

class OnboardedClient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    business_name = models.CharField(max_length=255)
    whatsapp_business_id = models.CharField(max_length=255, unique=True)
    access_token = models.TextField()  # The token from FB
    long_lived_token = models.TextField(null=True, blank=True)
    onboarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
