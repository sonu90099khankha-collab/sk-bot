import yt_dlp
import re
import os

def get_youtube_stream_url(query):
    if not query:
        return None
    
    query = str(query).strip()
    
    if "youtube.com" in query or "youtu.be" in query:
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', query)
        if match:
            query = f"https://www.youtube.com/watch?v={match.group(1)}"

    ydl_opts = {
        'format': 'bestaudio/bestaudio.webm/best',
        'noplaylist': True,
        'quiet': True,
        'skip_download': True,
        'geo_bypass': True,
        'default_search': 'ytsearch',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    search_target = query if ("youtube.com" in query or "youtu.be" in query) else f"ytsearch:{query}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = yt_dlp.YoutubeDL(ydl_opts).extract_info(search_target, download=False)
            
            if 'entries' in info and info['entries']:
                info = info['entries'][0]
                
            if info:
                # Check formats first for direct audio stream
                formats = info.get('formats', [])
                for f in formats:
                    if f.get('acodec') != 'none' and f.get('url') and 'googlevideo.com' in f.get('url'):
                        return f['url']
                
                # Check info url if it's a direct stream
                direct_url = info.get('url')
                if direct_url and 'googlevideo.com' in direct_url:
                    return direct_url
                    
                # Fallback to any valid format url
                for f in formats:
                    if f.get('url') and 'googlevideo.com' in f.get('url'):
                        return f['url']
                        
    except Exception as e:
        print(f"YT Handler Error: {e}")
        
    return None
  
