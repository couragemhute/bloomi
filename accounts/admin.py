# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Qualification, Profession, FacilitatorProfile, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "email",
        "role",
        "full_name",
        "phone_number",
        "is_staff",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "full_name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": (
                "full_name",
                "profile_picture",
                "phone_number",
            )
        }),
        ("Access Control", {
            "fields": (
                "role",                # ✅ ADD THIS
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": (
                "last_login",
                "created_at",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "role",          # ✅ ADD THIS
                "is_staff",
                "is_active",
            ),
        }),
    )

# --- Qualification Admin ---
@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'year_obtained')
    search_fields = ('name', 'institution')
    list_filter = ('year_obtained',)

# --- Profession Admin ---
@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# --- FacilitatorProfile Admin ---
@admin.register(FacilitatorProfile)
class FacilitatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_full_name')
    search_fields = ('user__email', 'user__full_name')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email"

    def user_full_name(self, obj):
        return obj.user.full_name
    user_full_name.short_description = "Full Name"

