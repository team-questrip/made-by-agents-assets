import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# Scopes required for uploading videos
SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']

CLIENT_SECRETS_FILE = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/client_secret.json'
TOKEN_FILE = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/token.json'

# The authorization code from the callback URL
AUTH_CODE = '4/0ASc3gC1Lqm3gvu1XWSznbqBj2q7D2UW6pm4JTZTNq3g9zQ1Eg4XtxPhgeGVmBCkjSTCyKg'

def finish_auth():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8080/')
    
    # Exchange the authorization code for an access token
    flow.fetch_token(code=AUTH_CODE)
    
    creds = flow.credentials
    
    # Save the credentials for the next run
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
            
    print("Authentication successful! Token saved to", TOKEN_FILE)

if __name__ == '__main__':
    finish_auth()
