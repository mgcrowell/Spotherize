import requests
import json
import creds # this is a secrets.py file, saves me the extra dependancy
import spothorize #imports auth flow from authorize.py
#API Vars
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1'

def process_liked_songs(json_data):
    return

#Authorize
auth_code = spothorize.get_authorization_code()
print(f'\nauth_code: {auth_code}')

request_token = spothorize.exchange_code_for_token(auth_code)
auth_token = request_token['access_token']
print(f'\nauth_token: {auth_token}\n')

params = {
    'limit': 10, 'offset': 0
}
# Perform the GET request for User ID
headers = {
    'Authorization': f'Bearer {auth_token}'
}
response = requests.get(f'{BASE_URL}/me', headers=headers)
if response.status_code == 200:
    results = response.json()
    user_id = results['id']
else:
    print(f"Failed with code: {response.status_code}")

# Perform the GET request for User Playlists
response = requests.get(f'{BASE_URL}/me/tracks',headers = headers)
if response.status_code == 200:
    results = response.json()

    print("\n\nLiked Songs:\n")
    print(json.dumps(results, indent=2))