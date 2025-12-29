from django.contrib import admin
from .models import Role

# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_admin')
    search_fields = ('name', 'code')
    filter_horizontal = ('permissions',)