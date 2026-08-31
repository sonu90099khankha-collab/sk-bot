import yt_dlp

def get_youtube_stream_url(query):
    if not query:
        return None
    
    # यदि आपने सीधे यूट्यूब का लिंक दिया है
    if "youtube.com" in query or "youtu.be" in query:
        return query
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'skip_download': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # सीधे यूट्यूब पर खोजें
            search_results = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' in search_results and len(search_results['entries']) > 0:
                song_info = search_results['entries'][0]
                return song_info.get('url') or f"https://www.youtube.com/watch?v={song_info.get('id')}"
    except Exception as e:
        print(f"Error: {e}")
        
    # अगर कभी सर्च ब्लॉक भी हो, तो यह एक डिफ़ॉल्ट गाना बजा देगा ताकि बोट अटके नहीं
    return "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    
