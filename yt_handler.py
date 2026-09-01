import yt_dlp
import re

def get_youtube_stream_url(query):
    if not query:
        return None
    
    # 1. Query ko string mein convert karein aur extra spaces hatayein
    query = str(query).strip()
    
    # 2. Agar user ne galti se double/nested link bhej diya hai, toh usko clean karke asli YouTube link nikalein
    urls = re.findall(r'(https?://[^\s]+)', query)
    if urls:
        # Sabse pehle valid YouTube URL ko dhoondhein
        for u in urls:
            if "youtu.be" in u or "youtube.com" in u:
                # Agar URL ke andar hi doosra URL ghusa hua hai, toh use thik karein
                clean_url = u.split('&')[0].split('?')[0] # Basic split ya cleanup
                if "youtu.be/" in u:
                    parts = u.split("youtu.be/")
                    if len(parts) > 1:
                        video_id = parts[-1].split('/')[0].split('?')[0].split('&')[0]
                        if video_id:
                            query = f"https://youtu.be/{video_id}"
                            break
                elif "watch?v=" in u:
                    parts = u.split("watch?v=")
                    if len(parts) > 1:
                        video_id = parts[-1].split('&')[0].split('/')[0]
                        if video_id:
                            query = f"https://www.youtube.com/watch?v={video_id}"
                            break

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['mweb', 'web', 'android']
                }
            },
            'geo_bypass': True,
            'socket_timeout': 15,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Agar clean karne ke baad bhi yeh valid URL nahi hai, toh ise YouTube search maan lo
            if not ("youtube.com" in query or "youtu.be" in query):
                search_target = f"ytsearch1:{query}"
            else:
                search_target = query

            info = ydl.extract_info(search_target, download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
            else:
                entry = info
                
            if entry:
                # Direct streaming format URL nikalna
                formats = entry.get('formats', [])
                for f in formats:
                    if f.get('acodec') != 'none' and f.get('url'):
                        return f['url']
                
                if 'url' in entry and entry['url']:
                    return entry['url']
                    
                video_id = entry.get('id')
                if video_id:
                    return f"https://www.youtube.com/watch?v={video_id}"
                    
    except Exception as e:
        print(f"Final Ironclad YT Handler Error: {e}")
        
    return None
          
