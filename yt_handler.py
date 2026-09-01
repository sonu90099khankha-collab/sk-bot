import yt_dlp
import re
import os

def get_youtube_stream_url(query):
    if not query:
        return None
    
    query = str(query).strip()
    
    # 1. Clean URL
    if "youtube.com" in query or "youtu.be" in query:
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', query)
        if match:
            video_id = match.group(1)
            query = f"https://www.youtube.com/watch?v={video_id}"

    # 2. Heavy Optimized Options for Fast Stream Fetching
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': False,
        'skip_download': True,
        'geo_bypass': True,
        'socket_timeout': 15,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'mweb', 'web']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    search_target = query if ("youtube.com" in query or "youtu.be" in query) else f"ytsearch1:{query}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_target, download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
            else:
                entry = info
                
            if entry:
                formats = entry.get('formats', [])
                for f in formats:
                    if f.get('acodec') != 'none' and f.get('url'):
                        return f['url']
                
                if 'url' in entry and entry['url']:
                    return entry['url']
                    
                vid = entry.get('id')
                if vid:
                    return f"https://www.youtube.com/watch?v={vid}"
                    
    except Exception as e:
        print(f"Fast YT Handler Error: {e}")
        
    return None
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
            video_id = match.group(1)
            query = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': False,
        'skip_download': True,
        'geo_bypass': True,
        'socket_timeout': 20,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'mweb', 'web', 'android']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    search_target = query if ("youtube.com" in query or "youtu.be" in query) else f"ytsearch1:{query}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_target, download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
            else:
                entry = info
                
            if entry:
                formats = entry.get('formats', [])
                for f in formats:
                    if f.get('acodec') != 'none' and f.get('url'):
                        return f['url']
                
                if 'url' in entry and entry['url']:
                    return entry['url']
                    
                vid = entry.get('id')
                if vid:
                    return f"https://www.youtube.com/watch?v={vid}"
                    
    except Exception as e:
        print(f"Heavy YT Handler Error: {e}")
        
    return None
        
