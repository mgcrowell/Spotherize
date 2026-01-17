# Spotherize - Spotify OAuth Flow
> A lightweight, dependency-free Python implementation of Spotify's OAuth 2.0 flow using only standard library modules. 

This single-file module handles the authorization process for the Spotify Web API.
```Python
import spothorize

# Get user authorization
auth_code = spotherize.get_authorization_code()

# Exchange for access token
access_token = spotherize.exchange_code_for_token(auth_code)
```
### How It Works
The auth flow is in the method get_authorization_code()
It creates a server for Spotify URI callback and returns an authorization code.
In your API console you must set Redirect URI to http://127.0.0.1:8888/callback
It then parses the URL for your authorization code and returns it to you

To get an access token, call exchange_code_for_token({auth_code}) and it will return your token to add to your header

### Examples
Check the repository for complete usage examples showing how to integrate this into your projects.


Feel free to reuse or copy/paste the code. Idc.
