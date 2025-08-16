# bot/views.py
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import OnboardedClient

@csrf_exempt
def exchange_fb_code(request):
    """
    Receives 'code' from the frontend and exchanges it for an access token
    """
    if request.method == "POST":
        data = json.loads(request.body)
        code = data.get("code")
        business_name = data.get("business_name", "Unknown")

        if not code:
            return JsonResponse({"error": "Code not provided"}, status=400)

        # Step 1: Exchange code for short-lived token
        token_url = "https://graph.facebook.com/v22.0/oauth/access_token"
        params = {
            "client_id": settings.FB_APP_ID,
            "client_secret": settings.FB_APP_SECRET,
            "redirect_uri": settings.FB_REDIRECT_URI,
            "code": code
        }
        r = requests.get(token_url, params=params)
        token_data = r.json()
        short_lived_token = token_data.get("access_token")

        if not short_lived_token:
            return JsonResponse({"error": token_data}, status=400)

        # Step 2: Exchange for long-lived token
        long_token_url = "https://graph.facebook.com/v22.0/oauth/access_token"
        long_params = {
            "grant_type": "fb_exchange_token",
            "client_id": settings.FB_APP_ID,
            "client_secret": settings.FB_APP_SECRET,
            "fb_exchange_token": short_lived_token
        }
        r_long = requests.get(long_token_url, params=long_params)
        long_token_data = r_long.json()
        long_lived_token = long_token_data.get("access_token", short_lived_token)

        # Step 3: Save to database
        client, _ = OnboardedClient.objects.update_or_create(
            whatsapp_business_id=data.get("business_id", "unknown_id"),
            defaults={
                "business_name": business_name,
                "access_token": short_lived_token,
                "long_lived_token": long_lived_token
            }
        )

        return JsonResponse({
            "message": "Client onboarded successfully",
            "access_token": short_lived_token,
            "long_lived_token": long_lived_token
        })
