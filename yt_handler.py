import yt_dlp

def get_youtube_stream_url(query):
    if not query:
        return None
    
    if "youtube.com" in query or "youtu.be" in query:
        return query
        
    try:
        # YouTube bot check ko bypass karne ke liye safest options aur clients
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'web']
                }
            },
            'skip_download': True,
            'geo_bypass': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Direct URL extraction search keyword ke through
            search_query = f"ytsearch1:{query}"
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
                
                # Agar direct streaming URL mil jaye
                if 'url' in entry and entry['url']:
                    return entry['url']
                
                # Agar formats list di gayi ho
                formats = entry.get('formats', [])
                for f in formats:
                    if f.get('acodec') != 'none' and f.get('url'):
                        return f['url']
                        
                # Last option video ID se URL banana
                video_id = entry.get('id')
                if video_id:
                    return f"https://www.youtube.com/watch?v={video_id}"
                    
    except Exception as e:
        print(f"YT-DLP Error: {e}")
        
    return None
    
