
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager
from blog.models import TimeStampMixin

# ------------------------
# Custom User Manager
# ------------------------
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


# ------------------------
# Custom User Model
# ------------------------
class CustomUser(AbstractUser, TimeStampMixin):
    username = None  # remove username
    email = models.EmailField(unique=True)

    # optional extras
    full_name = models.CharField(max_length=150, blank=True)
    profile_picture = models.ImageField(upload_to="users/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # removes username requirement

    objects = CustomUserManager()

    def __str__(self):
        return self.email