import requests
import json
import creds # this is a secrets.py file, saves me the extra dependancy
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
query = input("Enter an Artist Name to Search: ")
# Test Params
params = {
    'q': query,
    'type': 'artist',
    'limit': 1 # 1 result
}
# Perform the GET request
response = requests.get(f'{BASE_URL}/search?', headers=headers, params=params)
if response.status_code == 200:
    results = response.json()
    #print(json.dumps(results, indent=2))
    if results['artists']['items']:
        artist = results['artists']['items'][0]
        
        # Get name
        name = artist.get('name', 'Unknown Artist')
        
        # Get Spotify URL
        external_urls = artist.get('external_urls', {})
        spotify_url = external_urls.get('spotify', 'No URL available')
        
        print(f"\n--- Artist Information ---")
        print(f"Name: {name}")
        print(f"Spotify URL: {spotify_url}")
        print(f"ID: {artist.get('id', 'N/A')}")
        
        # Get all genres
        genres = artist.get('genres', [])
        if genres:
            print(f"Genres: {', '.join(genres)}")
        else:
            print("Genres: Not specified")
            
        # Get image (largest one)
        images = artist.get('images', [])
        if images:
            print(f"Profile Image: {images[0]['url']}")
    else:
        print("No artists found in the search results.")
else:
    print("Failed with code: {response.status_code}")