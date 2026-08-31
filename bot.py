import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import yt_dlp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped, VideoPiped

# Render port keep-alive server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "VCPlayerBot",
    api_id=int(API_ID) if API_ID else 0,
    api_hash=API_HASH or "",
    bot_token=BOT_TOKEN or ""
)

call_py = PyTgCalls(app)

def get_yt_url(query):
    ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
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
        "👋 VC Music & Video Bot is Online!\n\n"
        "🎵 Play Audio: /play <song name>\n"
        "📺 Play Video: /video <video name>\n"
        "⏹️ Stop: /stop"
    )
    await message.reply(text)

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please give a song name or YouTube link!")
    
    m = await message.reply("🔍 Searching song...")
    try:
        url = get_yt_url(query)
        if not url:
            return await m.edit("❌ Song not found!")
        
        await m.edit("🎵 Playing audio in Voice Chat...")
        await call_py.join_group_call(chat_id, AudioPiped(url))
    except Exception as e:
        await m.edit(f"❌ Error: {e}")

@app.on_message(filters.command("video"))
async def play_video(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please give a video name or YouTube link!")
    
    m =აზე message.reply("🔍 Searching video...")
    try:
        url = get_yt_url(query)
        if not url:
            return await m.edit("❌ Video not found!")
        
        await m.edit("📺 Playing video in Voice Chat...")
        await call_py.join_group_call(chat_id, VideoPiped(url))
    except Exception as e:
        await m.edit(f"❌ Error: {e}")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    chat_id = message.chat.id
    try:
        await call_py.leave_group_call(chat_id)
        await message.reply("⏹️ Stopped and left the voice chat.")
    except Exception as e:
        await message.reply(f"Error: {e}")

async def main():
    await app.start()
    await call_py.start()
    print("Bot is successfully running and connected!")
    await asyncio.gather()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
