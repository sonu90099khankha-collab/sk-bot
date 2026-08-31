import yt_dlp

def get_youtube_stream_url(query):
    if not query:
        return None
    
    if "youtube.com" in query or "youtu.be" in query:
        return query
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'skip_download': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' in search_results and len(search_results['entries']) > 0:
                song_info = search_results['entries'][0]
                return song_info.get('url') or f"https://www.youtube.com/watch?v={song_info.get('id')}"
    except Exception as e:
        print(f"YT Search Error: {e}")
        
    return "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    
