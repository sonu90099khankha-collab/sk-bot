import yt_dlp

def get_yt_url(query):
    ydl_opts = {
        "format": "bestaudio/best",
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
            
            search_query = f"ytsearch1:{query}"
            info = ydl.extract_info(search_query, download=False)
            
            if "entries" in info and len(info["entries"]) > 0:
                video_url = info["entries"][0]["url"]
                full_info = ydl.extract_info(video_url, download=False)
                return full_info.get("url")
                
        except Exception as e:
            print(f"Search error: {e}")
            
        try:
            fallback_query = f"ytsearch1:Hindi romantic songs jukebox" if "aashiqui" not in query.lower() else f"ytsearch1:Aashiqui 2 audio jukebox"
            info = ydl.extract_info(fallback_query, download=False)
            if "entries" in info and len(info["entries"]) > 0:
                video_url = info["entries"][0]["url"]
                full_info = ydl.extract_info(video_url, download=False)
                return full_info.get("url")
        except:
            pass
            
        return None
          
