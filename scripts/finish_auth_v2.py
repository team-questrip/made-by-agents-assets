from google_auth_oauthlib.flow import Flow

SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

CLIENT_SECRETS_FILE = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/client_secret.json'
TOKEN_FILE = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/token.json'

AUTH_CODE = '4/0ASc3gC0peavt11VJA5DgMZYIf8a4q6lz-P4gNtJVCGgqfqEgriBDdwqCQ1vreZ46tB-NTQ'

def finish_auth():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8080/')
    
    flow.fetch_token(code=AUTH_CODE)
    creds = flow.credentials
    
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
            
    print("Authentication successful! Token saved with comment permissions!")

if __name__ == '__main__':
    finish_auth()
