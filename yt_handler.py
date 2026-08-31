import yt_dlp
import urllib.parse
import urllib.request
import json
import re

def get_youtube_stream_url(query):
    if not query:
        return None
    
    # 1. If user gave a direct link
    if "youtube.com" in query or "youtu.be" in query:
        return query
        
    # 2. Try standard yt-dlp search first
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' in search_results and len(search_results['entries']) > 0:
                song_info = search_results['entries'][0]
                return song_info.get('url') or f"https://www.youtube.com/watch?v={song_info.get('id')}"
    except Exception:
        pass

    # 3. Fallback: DuckDuckGo / Web scraping search if yt-dlp fails due to blocking
    try:
        encoded_query = urllib.parse.quote(f"{query} youtube watch")
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Find first youtube watch link in search results
            match = re.search(r'href="(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)', html)
            if match:
                yt_url = match.group(1)
                # Extract stream url using yt_dlp from that link
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(yt_url, download=False)
                    return info.get('url') or yt_url
    except Exception:
        pass

    return None
                
