import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import asyncio
import yt_dlp
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls

# Safe import for AudioPiped and VideoPiped across different pytgcalls versions
try:
    from pytgcalls.types import AudioPiped, VideoPiped
except ImportError:
    try:
        from pytgcalls.types.input_stream import AudioPiped, VideoPiped
    except ImportError:
        from pytgcalls.types.input_stream.quality import AudioPiped, VideoPiped

# Fake web server to keep the port active on Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# Load credentials directly from Render environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "VCPlayerBot",
    api_id=int(API_ID) if API_ID else 0,
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
        "👋 Music & Video VC Bot is online!\n\n"
        "🎵 Play Audio: /play <song name or url>\n"
        "📺 Play Video: /video <video name or url>\n"
        "⏹️ Stop: /stop\n"
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
        
        await m.edit("🎵 Playing audio in VC...")
        await call_py.join_group_call(
            chat_id,
            AudioPiped(url)
        )
    except Exception as e:
        await m.edit(f"❌ Error: {e}\n\n💡 Make sure the bot is an Admin with 'Manage Video Chats' permission!")

@app.on_message(filters.command("video"))
async def play_video(client, message):
    chat_id, query = message.chat.id, " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a video name or YouTube link to play!")
    
    m = await message.reply("🔍 Searching...")
    try:
        url = get_yt_url(query)
        if not url:
            return await m.edit("❌ Video not found!")
        
        await m.edit("📺 Playing video in VC...")
        await call_py.join_group_call(
            chat_id,
            VideoPiped(url)
        )
    except Exception as e:
        await m.edit(f"❌ Error: {e}\n\n💡 Make sure the bot is an Admin with 'Manage Video Chats' permission!")

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
    
