# Spotherize 
## Python OAuth Flow for Spotify Web API built entirely using python standard library modules
A functional OAuth flow for spotify web API in one file
To use this, import the file into your python script and call it's auth and key exchange functions.
```Python
import spothorize
#Authorize
auth_code = spothorize.get_authorization_code()
request_token = spothorize.exchange_code_for_token(auth_code)
```
There are some examples in the repo as well.
