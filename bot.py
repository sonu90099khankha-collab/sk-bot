import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import asyncio
import yt_dlp
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, VideoPiped
import config
from config import API_ID, API_HASH, BOT_TOKEN

# Render ke liye chhota sa fake web server jo port pakad kar rakhega
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Server ko background me chala do taaki Render khush rahe
threading.Thread(target=run_server, daemon=True).start()

app = Client(
    "VCPlayerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

def get_yt_url(query):
    ydl_opts = {"format": "bestaudio/best", "noplaylist": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            if query.startswith("http"):
                info = ydl.extract_info(query, download=False)
                return info.get("url")
            else:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if "entries" in info:
                    return info["entries"][0]["url"]
        except Exception:
            pass
        return None

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    text = (
        "👋 **Music & Video VC Bot is online!**\n\n"
        "🎵 Play Audio: `/play <song name or url>`\n"
        "📺 Play Video: `/video <video name or url>`\n"
        "⏹️ Stop: `/stop`\n"
    )
    await message.reply(text, disable_web_page_preview=True)

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name or YouTube link to play!")
    
    m = await message.reply("🔍 Searching...")
    try:
        url = get_yt_url(query)
        if not url:
            return await m.edit("❌ Song not found!")
        
        await m.edit("🎵 Playing audio...")
        await call_py.join_group_call(
            chat_id,
            AudioPiped(url)
        )
    except Exception as e:
        await m.edit(f"Error: {e}")

@app.on_message(filters.command("video"))
async def play_video(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a video name or YouTube link to play!")
    
    m = await message.reply("🔍 Searching...")
    try:
        url = get_yt_url(query)
        if not url:
            return await m.edit("❌ Video not found!")
        
        await m.edit("📺 Playing video...")
        await call_py.join_group_call(
            chat_id,
            VideoPiped(url)
        )
    except Exception as e:
        await m.edit(f"Error: {e}")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    chat_id = message.chat.id
    try:
        await call_py.leave_group_call(chat_id)
        await message.reply("⏹️ Left the voice chat.")
    except Exception as e:
        await message.reply(f"Error: {e}")

if __name__ == "__main__":
    app.start()
    call_py.start()
    idle()
    
