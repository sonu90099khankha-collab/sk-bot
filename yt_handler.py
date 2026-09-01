import yt_dlp

def get_youtube_stream_url(query):
    if not query:
        return None
    
    # Agar user ne seedha YouTube ka link diya hai
    if "youtube.com" in query or "youtu.be" in query:
        return query
        
    try:
        # yt-dlp ka use karke real-time me YouTube se song search karke uska direct stream URL ya video link nikalna
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ytsearch1 matlab pehla sabse accha result uthayega
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video_url = info['entries'][0].get('url') or f"https://www.youtube.com/watch?v={info['entries'][0].get('id')}"
                return video_url
    except Exception as e:
        print(f"YT-DLP Search Error: {e}")
        
    return None
    
