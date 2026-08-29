import yt_dlp

def get_yt_url(query, is_video=False):
    # Faltu ke shabad hata kar sirf main naam nikalne ke liye
    cleaned_query = query.lower()
    for word in ["movie ke gane", "movie", "song", "songs", "video", "audio", "play", "gana", "gane", "ka", "ki"]:
        cleaned_query = cleaned_query.replace(word, "")
    cleaned_query = cleaned_query.strip()
    
    if not cleaned_query:
        cleaned_query = "Aashiqui 2 jukebox"

    ydl_format = "best/bestvideo+bestaudio" if is_video else "bestaudio/best"
    
    ydl_opts = {
        "format": ydl_format,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}}
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            if query.startswith("http"):
                info = ydl.extract_info(query, download=False)
                return info.get("url")
            
            search_query = f"ytsearch1:{cleaned_query} audio"
            info = ydl.extract_info(search_query, download=False)
            
            if "entries" in info and len(info["entries"]) > 0:
                video_url = info["entries"][0]["url"]
                full_info = ydl.extract_info(video_url, download=False)
                return full_info.get("url")
                
        except Exception as e:
            print(f"Search error: {e}")
            
        try:
            fallback_query = f"ytsearch1:Aashiqui 2 full album audio songs"
            info = ydl.extract_info(fallback_query, download=False)
            if "entries" in info and len(info["entries"]) > 0:
                video_url = info["entries"][0]["url"]
                full_info = ydl.extract_info(video_url, download=False)
                return full_info.get("url")
        except:
            pass
            
        return None
        
