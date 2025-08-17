# bot/views.py
import requests
import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import OnboardedClient

logger = logging.getLogger(__name__)

@csrf_exempt
def exchange_fb_code(request):
    logger.info("📩 Received request at /facebook-onboarding/exchange-code/")

    if request.method != "POST":
        logger.warning("❌ Invalid request method: %s", request.method)
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        data = json.loads(request.body)
        logger.debug("✅ Parsed JSON body: %s", data)
    except json.JSONDecodeError as e:
        logger.error("❌ Failed to decode JSON: %s", e)
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    code = data.get("code")
    business_name = data.get("business_name", "Unknown")
    business_id = data.get("business_id", "unknown_id")

    logger.info("➡️ Extracted values: code=%s..., business_name=%s, business_id=%s",
                code[:6] if code else None, business_name, business_id)

    if not code:
        logger.error("❌ No code provided in request body")
        return JsonResponse({"error": "Code not provided"}, status=400)

    # Step 1: Exchange code for short-lived token
    token_url = "https://graph.facebook.com/v22.0/oauth/access_token"
    params = {
        "client_id": settings.FB_APP_ID,
        "client_secret": settings.FB_APP_SECRET,
        "redirect_uri": settings.FB_REDIRECT_URI,
        "code": code
    }
    logger.info("🌐 Requesting short-lived token from Facebook: %s", token_url)
    r = requests.get(token_url, params=params)
    token_data = r.json()
    logger.debug("📩 FB short-lived token response: %s", token_data)

    short_lived_token = token_data.get("access_token")
    if not short_lived_token:
        logger.error("❌ Failed to retrieve short-lived token")
        return JsonResponse({"error": token_data}, status=400)

    # Step 2: Exchange for long-lived token
    long_token_url = "https://graph.facebook.com/v22.0/oauth/access_token"
    long_params = {
        "grant_type": "fb_exchange_token",
        "client_id": settings.FB_APP_ID,
        "client_secret": settings.FB_APP_SECRET,
        "fb_exchange_token": short_lived_token
    }
    logger.info("🌐 Requesting long-lived token from Facebook")
    r_long = requests.get(long_token_url, params=long_params)
    long_token_data = r_long.json()
    logger.debug("📩 FB long-lived token response: %s", long_token_data)

    long_lived_token = long_token_data.get("access_token", short_lived_token)

    # Step 3: Save securely in DB
    logger.info("💾 Saving OnboardedClient to DB (business_id=%s)", business_id)
    client, created = OnboardedClient.objects.update_or_create(
        whatsapp_business_id=business_id,
        defaults={
            "business_name": business_name,
            "access_token": short_lived_token,
            "long_lived_token": long_lived_token
        }
    )
    logger.info("✅ OnboardedClient saved: %s (created=%s)", client, created)

    return JsonResponse({
        "message": "Client onboarded successfully",
        "business_id": business_id,
        "business_name": business_name,
        "created": created
    })
