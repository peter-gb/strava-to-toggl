from dotenv import load_dotenv, set_key
import os
import requests
import json

# First need to get a access token
load_dotenv(override=True)

# Strava API Credentials
STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_ACCESS_TOKEN = os.getenv('STRAVA_ACCESS_TOKEN')
STRAVA_REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')

url_auth = "https://www.strava.com/oauth/token"

payload = {
    'grant_type' : "refresh_token",
    'client_id' : STRAVA_CLIENT_ID,
    'client_secret' : STRAVA_CLIENT_SECRET,
    'refresh_token' : STRAVA_REFRESH_TOKEN
}

response = requests.post(url_auth, data=payload)

tokens = response.json()
if tokens['refresh_token'] != STRAVA_REFRESH_TOKEN :       # token was refreshed by strava
    set_key(".env", "STRAVA_REFRESH_TOKEN", tokens["refresh_token"])
    print("Refresh token updated")
print("Refresh token OK, access token received")


token = tokens["access_token"]
headers = { 'Authorization': f'Bearer {token}'}

# Check logged in user
url_who = "https://www.strava.com/api/v3/athlete"
response = requests.get(url_who, headers=headers)
status = response.status_code

filename = 'data/athlete.json'
with open(filename, "w") as file:
    json.dump(response.json(), file)

# Get athlete stats
athlete_id = 11276947
url_athlete = f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats"

response = requests.get(url_athlete, headers=headers)

print(response.text)

filename = 'data/athlete_stats.json'
with open(filename, "w") as file:
    json.dump(response.json(), file)

# Now can fetch activities
#url = "https://strava.com/athlete/activities"
