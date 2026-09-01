import yt_dlp
import re

def get_youtube_stream_url(query):
    if not query:
        return None
    
    query = str(query).strip()
    
    # Clean any messy or double URLs if passed by user
    if "youtube.com" in query or "youtu.be" in query:
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', query)
        if match:
            video_id = match.group(1)
            query = f"https://www.youtube.com/watch?v={video_id}"

    try:
        # YouTube bot check ko bypass karne ke liye sabse latest clients aur options
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'mweb', 'web']
                }
            },
            'geo_bypass': True,
            'socket_timeout': 20,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_target = query if ("youtube.com" in query or "youtu.be" in query) else f"ytsearch1:{query}"
            
            info = ydl.extract_info(search_target, download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
            else:
                entry = info
                
            if entry:
                # Direct audio stream URL nikalna
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
        print(f"Bypass Error caught: {e}")
        
    return None
          
