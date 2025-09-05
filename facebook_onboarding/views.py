# bot/views.py
import json
import logging
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import OnboardedClient

logger = logging.getLogger(__name__)
GRAPH = getattr(settings, "FB_GRAPH_API_VERSION", "v23.0")


def fetch_facebook_token(url, params, token_type):
    """Helper to fetch tokens from Facebook Graph API."""
    try:
        logger.debug("🌍 Requesting %s token from %s", token_type, url)
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.debug("📡 %s token response: %s", token_type.capitalize(), data)
        return data
    except requests.RequestException as e:
        logger.error("❌ %s token request failed: %s", token_type.capitalize(), str(e))
        return {"error": str(e)}
    except ValueError:
        logger.error("❌ Invalid JSON response from Facebook (%s token)", token_type)
        return {"error": "Invalid JSON"}


def save_client(data, waba_id, business_name, phone_number_id, business_id, short_token=None, long_token=None):
    """Helper to save client onboarding details in DB."""
    client, created = OnboardedClient.objects.update_or_create(
        whatsapp_business_id=waba_id or business_id or "unknown",
        defaults={
            "business_name": business_name,
            "phone_number_id": phone_number_id,
            "business_id": business_id,
            "access_token": short_token,
            "long_lived_token": long_token,
            "meta": data,
        },
    )
    logger.info("💾 Client saved (created=%s): id=%s", created, client.pk)
    return client, created


@csrf_exempt
def exchange_fb_code(request):
    logger.info("🔵 /facebook-onboarding/exchange-code/ called")

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
        logger.debug("📥 Request JSON: %s", data)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    code = data.get("code")
    waba_id = data.get("waba_id") or data.get("whatsapp_business_id") or data.get("wabaId")
    phone_number_id = data.get("phone_number_id")
    business_id = data.get("business_id")
    business_name = data.get("business_name", "Unknown")
    note = data.get("note")

    logger.info(
        "➡️ Params extracted: code=%s, waba_id=%s, phone_number_id=%s, business_id=%s, business_name=%s",
        bool(code), waba_id, phone_number_id, business_id, business_name
    )

    # Case 1: No code, just save assets
    if not code:
        client, created = save_client(data, waba_id, business_name, phone_number_id, business_id)
        return JsonResponse({"message": "Saved WABA/phone ids (no code)", "waba_id": waba_id})

    # ---- Step 1: Short-lived token
    token_url = f"https://graph.facebook.com/{GRAPH}/oauth/access_token"
    short_data = fetch_facebook_token(token_url, {
        "client_id": settings.FB_APP_ID,
        "client_secret": settings.FB_APP_SECRET,
        "redirect_uri": settings.FB_REDIRECT_URI,
        "code": code
    }, "short-lived")

    short_token = short_data.get("access_token")
    if not short_token:
        return JsonResponse({"error": "token_exchange_failed", "details": short_data}, status=400)

    # ---- Step 2: Long-lived token
    long_data = fetch_facebook_token(token_url, {
        "grant_type": "fb_exchange_token",
        "client_id": settings.FB_APP_ID,
        "client_secret": settings.FB_APP_SECRET,
        "fb_exchange_token": short_token,
    }, "long-lived")

    long_token = long_data.get("access_token") or short_token

    # ---- Step 3: Save client
    client, created = save_client(
        {"short_token_response": short_data, "long_token_response": long_data, "raw_post": data},
        waba_id, business_name, phone_number_id, business_id,
        short_token, long_token
    )

    return JsonResponse({
        "message": "Client onboarded",
        "waba_id": client.whatsapp_business_id,
        "phone_number_id": client.phone_number_id,
        "created": created,
    })
