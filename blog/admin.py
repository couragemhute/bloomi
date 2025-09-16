# admin.py
from django.contrib import admin
from .models import Category, Blog

# ---------- Category Admin ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)

# ---------- Blog Admin ----------
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "content")
    list_filter = ("category", "created_at")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
