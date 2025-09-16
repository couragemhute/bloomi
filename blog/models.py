from django.db import models
from django.utils.text import slugify
from course.models import TimeStampMixin

class Category(TimeStampMixin):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Blog(TimeStampMixin):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="blogs")
    image = models.ImageField(upload_to="blogs/")
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subscriber(TimeStampMixin):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email