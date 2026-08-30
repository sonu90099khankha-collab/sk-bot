import yt_dlp

def get_yt_url(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "default_search": "ytsearch",
        "quiet": True,
        "extract_flat": False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            if not query.startswith("http"):
                query = f"ytsearch:{query}"
            info = ydl.extract_info(query, download=False)
            if "entries" in info:
                info = info["entries"][0]
            return info.get("url")
        except Exception as e:
            print(f"YTDLP Error: {e}")
            return None
  
