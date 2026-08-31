from yt_dlp import YoutubeDL

def get_youtube_stream_url(query):
    if not query:
        return None
    
    # If user directly provides a YouTube link
    if "youtube.com" in query or "youtu.be" in query:
        return query
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                return info['entries'][0]['url']
    except Exception as e:
        print(f"YouTube Search Error: {e}")
        
    return None
      
