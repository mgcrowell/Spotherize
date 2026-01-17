"""
Spothorize - A Python File for Spotify OAuth Flow
by: Michael Crowell

This code follows the spotify OAuth flow using python built-ins.
This code will get you private access to your spotify account, 
as well as a general 'Access Token' to use for querying public info
"""

import http.server
import socketserver
import urllib.parse
import webbrowser
from urllib.parse import urlparse, parse_qs
import threading
import time
import creds #this is part of creds.py and is NOT included with the repo
#Sporify OAuth Creds
CLIENT_ID = creds.client_id
CLIENT_SECRET = creds.client_secret
REDIRECT_URI = "http://127.0.0.1:8888/callback" # MAKE SURE YOU REGISTER THIS INTO YOUR SPOTIFY DEV CONSOLE!
SCOPES = "user-read-private user-read-email user-library-read"

#Globals for auth
auth_code = None
auth_state = None

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code,auth_state
        #Parse the URL
        parsed_url = urlparse(self.path)

        if parsed_url.path == '/callback':
            #Parse query params
            query_params = parse_qs(parsed_url.query)

            #Extract the auth code
            if 'code' in query_params:
                auth_code = query_params['code'][0]
                print(f"Auth code recieved: {auth_code}")
                if 'state' in query_params:
                    auth_state = query_params['state'][0]
                #Send success to the browser
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(
                    b"""
                    <html><body>
                    <h1>Authentication Successful</h1>
                    <p>You can close this page now.</p>
                    </body></html>
                    """)
                #Stopping the server after code get
                threading.Thread(target=self.server.shutdown).start()
            else: 
                #Handle error
                if 'error' in query_params:
                    error = query_params['error'][0]
                    print(f"Error received: {error}")
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"<h1>Error: {error}</h1>".encode())

        else:
            #Handle erroneous paths
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>What are you doing here?</h1>")

def start_server(port=8888):
    """Start server for OAuth Callback"""
    with socketserver.TCPServer(("", port), OAuthHandler) as httpd:
        print(f'Serving at port {port}')
        httpd.serve_forever()
def get_authorization_code():
    global auth_code

    #start server in a thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    #Give server some time to start
    time.sleep(1)

    # Construct the auth URL based on what Spotify expects
    auth_url = (
        f"https://accounts.spotify.com/authorize?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"scope={urllib.parse.quote(SCOPES)}&"
        f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}&"
        f"state=some_random_state_string"
    )
    print(auth_url)
    #Open Browser
    webbrowser.open(auth_url)

    #Wait for auth code
    while auth_code is None:
        time.sleep(0.1)
    return auth_code

def exchange_code_for_token(auth_code):
    """Exchange authorization code for access token"""
    import requests
    import base64
    
    # Prepare the token request
    token_url = "https://accounts.spotify.com/api/token"
    
    # Create the authorization header
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    
    # Make the request
    response = requests.post(token_url, headers=headers, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")
        
        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")
        print(f"Expires in: {expires_in} seconds")
        
        return token_data
    else:
        print(f"Error exchanging code for token: {response.status_code}")
        print(response.text)
        return None

# Main execution
if __name__ == "__main__":
    # Get the authorization code
    code = get_authorization_code()
    print(f"\nCaptured authorization code: {code}")
    
    # Exchange code for token (requires CLIENT_SECRET)
    # Uncomment and fill in your client secret to use this
    # token_data = exchange_code_for_token(code)
    
    # You can now use the access token to make API calls
    # Example: Get current user's profile
    # headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    # response = requests.get("https://api.spotify.com/v1/me", headers=headers)