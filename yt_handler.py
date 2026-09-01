import urllib.request
import urllib.parse
import json

def get_youtube_stream_url(query):
    if not query:
        return None
    
    if "youtube.com" in query or "youtu.be" in query:
        return query
        
    try:
        # Properly encodes the query to prevent ascii codec errors with Hindi or special characters
        encoded_query = urllib.parse.quote(query)
        
        # Using a stable Invidious instance API
        api_url = f"https://vid.puffyan.us/api/v1/search?q={encoded_query}&type=video"
        
        req = urllib.request.Request(
            api_url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0:
                video_id = data[0].get('videoId')
                if video_id:
                    return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"API Search Error: {e}")
        
    return "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
  
