# fetch_waba_info.py

import requests
import logging

# ----------------------------
# CONFIG
# ----------------------------
GRAPH = "v23.0"
LONG_LIVED_TOKEN = "EAAJWpfTUbNUBPR1jK6iOZCsCqnZBh13dm2fKPC26y84QKS3FHYaCA3lSXcBoqZBmrHj47qsARJKw5KdL2908BhfFFGwOPUZAoEHIbGyZBKxMFD8K5g1NoPGNGbmb5qMFTNWkdMHn1LUyUMFu31FdsEMkZBdMFMKER5bmMvgZAlB1ZA5gtVkFoRGEeshgnUZBl4TsQ"

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def get_whatsapp_business_accounts(token):
    url = f"https://graph.facebook.com/{GRAPH}/me"
    params = {
        "fields": "whatsapp_business_accounts",
        "access_token": token
    }
    logger.info("Fetching WhatsApp Business Accounts...")
    resp = requests.get(url, params=params).json()
    logger.debug("Response: %s", resp)

    waba_list = resp.get("whatsapp_business_accounts", {}).get("data", [])
    if not waba_list:
        logger.warning("No WhatsApp Business Accounts found for this token!")
        return None

    logger.info("Found WABAs: %s", [waba.get("id") for waba in waba_list])
    return waba_list[0]["id"]  # return first WABA ID

def get_waba_details(waba_id, token):
    url = f"https://graph.facebook.com/{GRAPH}/{waba_id}"
    params = {
        "fields": "name,phone_numbers,business,primary_owner",
        "access_token": token
    }
    logger.info("Fetching WABA details for ID: %s", waba_id)
    resp = requests.get(url, params=params).json()
    logger.debug("WABA details response: %s", resp)

    business_name = resp.get("name")
    business_id = resp.get("business", {}).get("id") if resp.get("business") else None
    phone_numbers = resp.get("phone_numbers", {}).get("data") if resp.get("phone_numbers") else []
    phone_number_id = phone_numbers[0]["id"] if phone_numbers else None
    owner_id = resp.get("primary_owner", {}).get("id") if resp.get("primary_owner") else None

    logger.info("✅ Fetched details:")
    logger.info("Business Name: %s", business_name)
    logger.info("WABA ID: %s", waba_id)
    logger.info("Business ID: %s", business_id)
    logger.info("Phone Number ID: %s", phone_number_id)
    logger.info("Owner User ID: %s", owner_id)

    return {
        "business_name": business_name,
        "waba_id": waba_id,
        "business_id": business_id,
        "phone_number_id": phone_number_id,
        "owner_id": owner_id
    }

if __name__ == "__main__":
    try:
        waba_id = get_whatsapp_business_accounts(LONG_LIVED_TOKEN)
        if not waba_id:
            logger.error("❌ Could not fetch WABA ID. Ensure the token has 'whatsapp_business_management' permission and is an admin.")
        else:
            details = get_waba_details(waba_id, LONG_LIVED_TOKEN)
    except Exception as e:
        logger.exception("❌ Error fetching WABA info: %s", e)
