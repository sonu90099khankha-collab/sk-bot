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
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'skip_download': True,
        'geo_bypass': True,
        'extractor_args': {'youtube': {'player_client': ['ios', 'mweb', 'web', 'android']}},
        'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    target = query if ("youtube.com" in query or "youtu.be" in query) else f"ytsearch1:{query}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target, download=False)
            entry = info['entries'][0] if 'entries' in info and info['entries'] else info
            
            if entry:
                for f in entry.get('formats', []):
                    if f.get('acodec') != 'none' and f.get('url'):
                        return f['url']
                if entry.get('url'):
                    return entry['url']
                if entry.get('id'):
                    return f"https://www.youtube.com/watch?v={entry['id']}"
    except Exception as e:
        print(f"Error: {e}")
        
    return None
    
