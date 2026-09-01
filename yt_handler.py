import yt_dlp
import re
import os

def get_youtube_stream_url(query):
    if not query:
        return None
    
    query = str(query).strip()
    
    # 1. Clean URL to exact 11-character Video ID
    if "youtube.com" in query or "youtu.be" in query:
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', query)
        if match:
            video_id = match.group(1)
            query = f"https://www.youtube.com/watch?v={video_id}"

    # 2. Ultra-Heavy Human Mimicry Configuration (Looks 100% like a real Chrome Browser)
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': False,
        'skip_download': True,
        'geo_bypass': True,
        'geo_bypass_country': 'IN',
        'socket_timeout': 30,
        'nocheckcertificate': True,
        
        # Sabhi authentic human clients ki heavy rotation
        'extractor_args': {
            'youtube': {
                'player_client': ['web', 'android', 'ios', 'mweb'],
                'skip': ['hls', 'dash']
            }
        },
        
        # Asli Windows Chrome browser ke powerful headers taaki YouTube bot detector andha ho jaye
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
        }
    }

    # Agar cookies.txt file maujood hai toh premium user ki tarah behave karega
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    # 3. Double-Layer Execution Guard (Agar ek tareeka fail ho, toh doosra automatically chal padega)
    search_targets = []
    if "youtube.com" in query or "youtu.be" in query:
        search_targets = [query]
    else:
        # Do alag-alag search queries taaki 100% match mile
        search_targets = [f"ytsearch1:{query}", f"ytsearch1:{query} audio song"]

    for target in search_targets:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(target, download=False)
                
                if 'entries' in info and len(info['entries']) > 0:
                    entry = info['entries'][0]
                else:
                    entry = info
                    
                if entry:
                    # Direct audio formats extraction
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
            print(f"⚠️ Layer failed for {target}: {e}")
            continue
            
    return None
  
