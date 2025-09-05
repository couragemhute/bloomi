# bot/views.py
import json
import requests
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import OnboardedClient

logger = logging.getLogger(__name__)

GRAPH = getattr(settings, "FB_GRAPH_API_VERSION", "v23.0")


@csrf_exempt
def exchange_fb_code(request):
    logger.info("🔵 Received request at /facebook-onboarding/exchange-code/")

    if request.method != "POST":
        logger.warning("❌ Invalid method: %s", request.method)
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
        logger.debug("📥 Raw request JSON: %s", data)
    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON in request body: %s", request.body)
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    code = data.get("code")
    waba_id = data.get("waba_id") or data.get("whatsapp_business_id") or data.get("wabaId")
    phone_number_id = data.get("phone_number_id")
    business_id = data.get("business_id")
    business_name = data.get("business_name", "Unknown")
    note = data.get("note")

    logger.info(
        "➡️ Extracted params: code=%s, waba_id=%s, phone_number_id=%s, business_id=%s, business_name=%s",
        bool(code), waba_id, phone_number_id, business_id, business_name
    )

    # Case 1: No code, just asset IDs
    if not code:
        logger.warning("⚠️ No 'code' provided, saving only asset IDs...")
        client, created = OnboardedClient.objects.update_or_create(
            whatsapp_business_id=waba_id,
            defaults={
                "business_name": business_name,
                "phone_number_id": phone_number_id,
                "business_id": business_id,
                "meta": data
            }
        )
        logger.info("💾 Saved asset-only client: id=%s created=%s", client.pk, created)
        return JsonResponse({"message": "Saved WABA/phone ids (no code)", "waba_id": waba_id})

    # Case 2: Code provided, exchange for tokens
    try:
        # Step 1: Code -> Short-lived token
        token_url = f"https://graph.facebook.com/{GRAPH}/oauth/access_token"
        params = {
            "client_id": settings.FB_APP_ID,
            "client_secret": settings.FB_APP_SECRET,
            "redirect_uri": settings.FB_REDIRECT_URI,
            "code": code
        }
        logger.debug("🌍 Requesting short-lived token: %s", token_url)
        r = requests.get(token_url, params=params, timeout=10)
        r.raise_for_status()
        token_data = r.json()
        logger.debug("📡 Short token response: %s", token_data)
    except requests.RequestException as e:
        logger.error("❌ Request error during short-lived exchange: %s", e)
        return JsonResponse({"error": "short_token_request_failed", "details": str(e)}, status=502)

    short_lived_token = token_data.get("access_token")
    if not short_lived_token:
        logger.error("❌ Short-lived token exchange failed: %s", token_data)
        return JsonResponse({"error": "token_exchange_failed", "details": token_data}, status=400)

    logger.info("✅ Short-lived token acquired")

    # Step 2: Short-lived -> Long-lived
    try:
        long_token_url = f"https://graph.facebook.com/{GRAPH}/oauth/access_token"
        long_params = {
            "grant_type": "fb_exchange_token",
            "client_id": settings.FB_APP_ID,
            "client_secret": settings.FB_APP_SECRET,
            "fb_exchange_token": short_lived_token
        }
        logger.debug("🌍 Requesting long-lived token...")
        r2 = requests.get(long_token_url, params=long_params, timeout=10)
        r2.raise_for_status()
        long_data = r2.json()
        logger.debug("📡 Long token response: %s", long_data)
    except requests.RequestException as e:
        logger.error("❌ Request error during long-lived exchange: %s", e)
        return JsonResponse({"error": "long_token_request_failed", "details": str(e)}, status=502)

    long_lived_token = long_data.get("access_token") or short_lived_token
    logger.info("✅ Long-lived token acquired")

    # Step 3: Save to DB
    client, created = OnboardedClient.objects.update_or_create(
        whatsapp_business_id=waba_id or business_id or "unknown",
        defaults={
            "business_name": business_name,
            "phone_number_id": phone_number_id,
            "access_token": short_lived_token,
            "long_lived_token": long_lived_token,
            "meta": {
                "short_token_response": token_data,
                "long_token_response": long_data,
                "raw_post": data
            }
        }
    )

    logger.info("💾 Onboarded client saved: id=%s created=%s", client.pk, created)
    return JsonResponse({
        "message": "Client onboarded",
        "waba_id": client.whatsapp_business_id,
        "phone_number_id": client.phone_number_id,
        "created": created
    })
