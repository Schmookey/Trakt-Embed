# refresh_trakt_token.py
import requests
import os
import sys

CLIENT_ID = os.getenv('TRAKT_CLIENT_ID')
CLIENT_SECRET = os.getenv('TRAKT_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('TRAKT_REFRESH_TOKEN')

# This redirect_uri must match EXACTLY what you set in your Trakt API App settings
# For device auth, it's typically 'urn:ietf:wg:oauth:2.0:oob'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
    print("Error: Missing one or more required environment variables (TRAKT_CLIENT_ID, TRAKT_CLIENT_SECRET, TRAKT_REFRESH_TOKEN)")
    sys.exit(1)

data = {
    'refresh_token': REFRESH_TOKEN,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'refresh_token'
}

response = requests.post('https://api.trakt.tv/oauth/token', json=data)

if response.status_code == 200:
    token_data = response.json()
    new_access_token = token_data['access_token']
    new_refresh_token = token_data.get('refresh_token', REFRESH_TOKEN) # Trakt might not always send a new refresh token
    expires_in = token_data['expires_in']
    
    print(f"NEW_ACCESS_TOKEN={new_access_token}")
    print(f"NEW_REFRESH_TOKEN={new_refresh_token}")
    print(f"EXPIRES_IN={expires_in}")
    print("Token refreshed successfully.")
else:
    print(f"Error refreshing token: {response.status_code}")
    print(response.text)
    sys.exit(1)