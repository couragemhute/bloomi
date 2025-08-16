from django.contrib import admin
from .models import OnboardedClient

@admin.register(OnboardedClient)
class OnboardedClientAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'whatsapp_business_id', 'onboarded_at')
    readonly_fields = ('onboarded_at',)
    search_fields = ('business_name', 'whatsapp_business_id')
