import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes required for uploading videos
SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']

CLIENT_SECRETS_FILE = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/client_secret.json'
TOKEN_FILE = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/token.json'

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            # Run local server for auth
            # Since this is running on the user's machine (host), we can use a fixed port like 8080
            creds = flow.run_local_server(port=8080)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
    print("Authentication successful! Token saved to", TOKEN_FILE)

if __name__ == '__main__':
    authenticate()
