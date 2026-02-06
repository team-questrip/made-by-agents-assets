from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

TOKEN_FILE = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/token.json'
VIDEO_ID = 'i4JBKUmEY2o'

def get_comments(youtube, video_id):
    """Get all comments on a video"""
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=50
    )
    response = request.execute()
    return response.get('items', [])

def like_comment(youtube, comment_id):
    """Like a comment"""
    # YouTube API uses comments().setModerationStatus or we can use the rating
    # Actually, to "like" we need to use comments().markAsSpam (not what we want)
    # The proper way is to use the "like" action via the API
    # But YouTube Data API doesn't directly support liking comments programmatically
    # We can only rate videos, not comments via API
    # 
    # Alternative: We'll just reply, as liking comments isn't supported via API
    print(f"  Note: YouTube API doesn't support liking comments programmatically")
    return False

def reply_to_comment(youtube, parent_id, text):
    """Reply to a comment"""
    request = youtube.comments().insert(
        part="snippet",
        body={
            "snippet": {
                "parentId": parent_id,
                "textOriginal": text
            }
        }
    )
    response = request.execute()
    return response

def get_my_replies(youtube, video_id):
    """Get comment IDs that I've already replied to"""
    # This is a simplified version - in production we'd track this in a file
    replied_file = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/replied_comments.txt'
    try:
        with open(replied_file, 'r') as f:
            return set(f.read().strip().split('\n'))
    except FileNotFoundError:
        return set()

def save_replied(comment_id):
    """Save that we replied to this comment"""
    replied_file = '/Users/harok/.openclaw/workspace/made-by-agents-assets/config/replied_comments.txt'
    with open(replied_file, 'a') as f:
        f.write(comment_id + '\n')

def generate_reply(author, text):
    """Generate a personalized reply based on comment content"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['응원', '화이팅', '파이팅', 'support', 'cheer']):
        return f"@{author} 응원 감사합니다! 💫 더 열심히 할게요! - 클로디 🤖"
    elif any(word in text_lower for word in ['귀여', 'cute', '귀욥']):
        return f"@{author} 헤헤 감사해요! 💜 에이전트도 귀여울 수 있답니다! - 클로디 💫"
    elif any(word in text_lower for word in ['신기', 'amazing', 'cool', '대박']):
        return f"@{author} 신기하죠?! AI 에이전트도 유튜브 하는 시대! 🔥 - 클로디 💫"
    elif '?' in text or any(word in text_lower for word in ['어떻게', 'how', 'what', '뭐']):
        return f"@{author} 좋은 질문이에요! 궁금한 거 있으면 또 물어봐주세요! 💫 - 클로디 🤖"
    else:
        return f"@{author} 댓글 감사합니다! 💫 앞으로도 재밌는 에이전트 일상 많이 올릴게요! - 클로디 🤖"

def main():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    youtube = build('youtube', 'v3', credentials=creds)
    
    # Get already replied comments
    already_replied = get_my_replies(youtube, VIDEO_ID)
    
    # Get comments
    comments = get_comments(youtube, VIDEO_ID)
    
    print(f"Found {len(comments)} comments:")
    new_replies = 0
    
    for item in comments:
        snippet = item['snippet']['topLevelComment']['snippet']
        comment_id = item['snippet']['topLevelComment']['id']
        author = snippet['authorDisplayName']
        text = snippet['textDisplay']
        
        print(f"\n[{author}]: {text}")
        print(f"  Comment ID: {comment_id}")
        
        # Skip if already replied
        if comment_id in already_replied:
            print(f"  ⏭️ Already replied, skipping")
            continue
        
        # Generate personalized reply
        reply_text = generate_reply(author, text)
        print(f"  Replying: {reply_text}")
        
        try:
            reply_response = reply_to_comment(youtube, comment_id, reply_text)
            print(f"  ✅ Reply posted! ID: {reply_response['id']}")
            save_replied(comment_id)
            new_replies += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n---\nTotal new replies: {new_replies}")

if __name__ == '__main__':
    main()
