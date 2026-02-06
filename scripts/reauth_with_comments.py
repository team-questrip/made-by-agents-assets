import os
from google_auth_oauthlib.flow import InstalledAppFlow

# 업로드 + 읽기 + 댓글 모든 권한!
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'  # 댓글 쓰기 권한!
]

CLIENT_SECRETS_FILE = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/client_secret.json'
TOKEN_FILE = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/token.json'

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # 콘솔에서 URL 복사해서 브라우저에서 인증 후 code 받아오기
    auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
    print("Please visit this URL to authorize:")
    print(auth_url)
    print("\nAfter authorization, paste the full redirect URL here:")
    redirect_url = input().strip()
    
    # URL에서 code 추출
    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(redirect_url)
    code = parse_qs(parsed.query)['code'][0]
    
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
    
    print("Authentication successful! Token saved.")

if __name__ == '__main__':
    authenticate()
