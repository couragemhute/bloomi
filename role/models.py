from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

from helpers.timestamp import TimestampMixin

# Create your models here.
class Role(TimestampMixin):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_admin and Role.objects.filter(is_admin=True).exclude(pk=self.pk).exists():
            raise ValueError("Only one role can be marked as admin")
        super().save(*args, **kwargs)
