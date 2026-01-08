from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from blog.models import TimeStampMixin
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, TimeStampMixin):
    username = None  # remove username
    email = models.EmailField(unique=True)
    role = models.ForeignKey('role.Role', on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)  # ✅ new field
    profile_picture = models.ImageField(upload_to="users/", blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Qualification(models.Model):
    """Store academic qualifications like degrees, diplomas, certifications."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="facilitator_qualification", null=True, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    year_obtained = models.PositiveIntegerField(null=True, blank=True)
    certificate = models.FileField(upload_to="facilitator_certificates/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.institution})"


class Profession(models.Model):
    """Store professions or areas of expertise."""
    name = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="facilitator_profession",null=True, blank=True)

    def __str__(self):
        return self.name


class FacilitatorProfile(models.Model):
    """Extra profile for a facilitator."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="facilitator_profile")
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.full_name}"
