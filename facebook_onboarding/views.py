# bot/views.py
import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import facebook
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


    try:
        # Step 2: Exchange short-lived -> long-lived token
        graph = facebook.GraphAPI(access_token=code)
        long_lived_token_info = graph.extend_access_token(settings.FB_APP_ID, settings.APP_SECRET)
        long_lived_token = long_lived_token_info.get("access_token")
        logger.info("✅ Long-lived token acquired")
    except facebook.GraphAPIError as e:
        logger.error("❌ Error extending token: %s", e)
        return JsonResponse({"error": "extend_token_failed", "details": str(e)}, status=502)

    # Step 3: Save to DB
    client, created = OnboardedClient.objects.update_or_create(
        whatsapp_business_id=waba_id or business_id or "unknown",
        defaults={
            "business_name": business_name,
            "phone_number_id": phone_number_id,
            "access_token": code,
            "long_lived_token": long_lived_token,
            "meta": {
                "short_token_response": {"access_token": code},
                "long_token_response": long_lived_token_info,
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
