import requests
import json
import creds # this is a secrets.py file, saves me the extra dependancy
import authroize #imports auth flow from authorize.py
#API Vars
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1'

#get the token
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': creds.client_id,
    'client_secret': creds.client_secret
})

auth_reponse_json = auth_response.json()

access_token = auth_reponse_json['access_token']
headers = {
    'Authorization': f'Bearer {access_token}'
}

#Authorize
redirect_uri = 'http://127.0.0.1/'
user_auth = requests.get()
# POST Params
params = {
    'limit': 10, 'offset': 0
}
# Perform the GET request
response = requests.get(f'{BASE_URL}/me', headers=headers)
if response.status_code == 200:
    results = response.json()
    print(json.dumps(results, indent=2))
else:
    print(f"Failed with code: {response.status_code}")