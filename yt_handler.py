import yt_dlp

def get_youtube_stream_url(query):
    if not query:
        return None
    
    if "youtube.com" in query or "youtu.be" in query:
        return query
        
    try:
        # YouTube ki bot-check (Sign in error) ko bypass karne ke liye advanced options
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'geo_bypass': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch1:{query}"
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
                # Direct streaming format URL nikalna taaki PyTgCalls bina kisi error ke chala sake
                formats = entry.get('formats', [])
                for f in formats:
                    if f.get('acodec') != 'none' and f.get('url'):
                        return f['url']
                
                # Fallback to general url if direct audio format not found
                return entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
    except Exception as e:
        print(f"YT-DLP Search & Extract Error: {e}")
        
    return None
    
