# extend_fb_token.py

from core import settings
import facebook

# Replace these with your actual values
SHORT_LIVED_TOKEN = "EAAJWpfTUbNUBPV9Nd440hGKI6DuHOt0UyAkeUmJf4yLf1CWZBFXwycqpKfLjmDLAaGhFeGyoSiSr8JzcYZCxZA1o7iKV6aheUlN4aKK8xPFFUSoGfFQnXPQUEifP52fofub3XluxYVh8s7ZAbyIXrN2HXXot6mZAIMdKdzWGoHDzHQJJJfsLyyPiAauZBzOXN21UmW4jkj7x4ZAJwvlxrPZBYa20bAl0zF34ZBwFi"
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
