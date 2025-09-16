from django.db import models
from django.utils.text import slugify


class TimeStampMixin(models.Model):
    """Reusable timestamp fields for created/updated tracking"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Course(TimeStampMixin):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="courses/")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Expert(TimeStampMixin):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="experts/")

    def __str__(self):
        return self.name
