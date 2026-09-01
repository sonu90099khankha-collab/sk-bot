import yt_dlp

def get_youtube_stream_url(query):
    if not query:
        return None
    
    # Agar user ne poora link bhi diya hai toh usko clean karke sahi kar lo
    query = query.strip()
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['mweb', 'web']
                }
            },
            'geo_bypass': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Agar seedha URL hai toh direct extract karo, nahi toh ytsearch karo
            search_target = query if ("youtube.com" in query or "youtu.be" in query) else f"ytsearch1:{query}"
            
            info = ydl.extract_info(search_target, download=False)
            
            # Agar playlist ya search result hai
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
                
                # Agar formats na mile toh direct entry ka url
                if 'url' in entry and entry['url']:
                    return entry['url']
                    
                # Last option video ID se URL banana
                video_id = entry.get('id')
                if video_id:
                    return f"https://www.youtube.com/watch?v={video_id}"
                    
    except Exception as e:
        print(f"YT Handler Final Error: {e}")
        
    return None
  
