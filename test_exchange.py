# extend_fb_token.py

import facebook
from django.conf import settings

# Replace these with your actual values
SHORT_LIVED_TOKEN = ""
APP_ID = settings.FB_APP_ID
APP_SECRET = settings.APP_SECRET

try:
    # Initialize Graph API with the short-lived token
    graph = facebook.GraphAPI(access_token=SHORT_LIVED_TOKEN)

    # Exchange for long-lived token
    long_lived_token_info = graph.extend_access_token(APP_ID, APP_SECRET)
    long_lived_token = long_lived_token_info.get('access_token')
    
    print("✅ Long-lived token acquired!")
    print("Long-lived token:", long_lived_token)

except facebook.GraphAPIError as e:
    print("❌ Error extending token:", e)
