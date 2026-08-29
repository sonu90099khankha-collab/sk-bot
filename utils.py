import yt_dlp

def get_yt_url(query, is_video=False):
    # Agar user ne kuch nahi diya toh default gaana set kar diya
    if not query or len(query.strip()) == 0:
        query = "Hindi romantic songs jukebox"

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
            # Agar seedha link diya hai
            if query.startswith("http"):
                info = ydl.extract_info(query, download=False)
                return info.get("url")
            
            # 1. Pehle user ki query par direct search marega
            search_query = f"ytsearch1:{query}"
            info = ydl.extract_info(search_query, download=False)
            
            if "entries" in info and len(info["entries"]) > 0:
                video_url = info["entries"][0]["url"]
                full_info = ydl.extract_info(video_url, download=False)
                return full_info.get("url")
                
        except Exception as e:
            print(f"Search error 1: {e}")
            
        try:
            # 2. Agar pehli baar mein nahi mila, toh aage "audio song" jod kar dobara koshish karega
            retry_query = f"ytsearch1:{query} audio song"
            info = ydl.extract_info(retry_query, download=False)
            if "entries" in info and len(info["entries"]) > 0:
                video_url = info["entries"][0]["url"]
                full_info = ydl.extract_info(video_url, download=False)
                return full_info.get("url")
        except Exception as e:
            print(f"Search error 2: {e}")

        try:
            # 3. Agar fir bhi fail ho gaya, toh fallback ke taur par super hit jukebox chala dega taaki gana band na ho
            fallback_query = f"ytsearch1:Aashiqui 2 full album audio songs"
            info = ydl.extract_info(fallback_query, download=False)
            if "entries" in info and len(info["entries"]) > 0:
                video_url = info["entries"][0]["url"]
                full_info = ydl.extract_info(video_url, download=False)
                return full_info.get("url")
        except:
            pass
            
        return None
        
