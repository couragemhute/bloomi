# admin.py
from django.contrib import admin

from blog.models import Subscriber
from .models import Course, Expert

# ---------- Course Admin ----------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "price", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")
    list_filter = ("level", "created_at")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

# ---------- Subscriber Admin ----------
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

# ---------- Expert Admin ----------
@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ("course", "user", "created_at")
    search_fields = ("course", "user")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
