import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from pyrogram import Client, filters

try:
    from vc_handler import setup_vc_calls
    VC_AVAILABLE = True
except Exception:
    VC_AVAILABLE = False

try:
    from yt_handler import get_youtube_stream_url
    YT_AVAILABLE = True
except Exception:
    YT_AVAILABLE = False

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), server_class=SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")

# Using a new session name to avoid old file conflicts and errors
if STRING_SESSION:
    app = Client(
        "sk_bot_v2",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION
    )
else:
    app = Client(
        "sk_bot_v2",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

call_py = None
if VC_AVAILABLE:
    try:
        call_py = setup_vc_calls(app)
    except Exception:
        call_py = None

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    text = (
        "🎵 **Audio/Video VC Bot is Live!**\n\n"
        "• Use `/play <song name>` for audio.\n"
        "• Use `/vplay <song name>` for video/stream."
    )
    await message.reply(text)

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name! Example: `/play Stay`")
    
    m = await message.reply("🔍 Searching audio...")
    
    if not YT_AVAILABLE:
        return await m.edit("Search handler is missing.")
    
    url = get_youtube_stream_url(query)
    if not url:
        return await m.edit("Song not found.")
    
    if not VC_AVAILABLE or not call_py:
        return await m.edit("Song found, but Voice Chat module is inactive.")
    
    await m.edit("🎧 Connecting to Voice Chat...")
    
    from vc_handler import start_vc_player
    success = await start_vc_player(call_py, chat_id, url, is_video=False)
    if success:
        await m.edit("▶️ Playing audio in VC!")
    else:
        await m.edit("❌ Failed to join Voice Chat. Make sure VC is active and Userbot is inside.")

@app.on_message(filters.command("vplay"))
async def play_video(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a video name! Example: `/vplay Pathaan`")
    
    m = await message.reply("🔍 Searching video...")
    
    if not YT_AVAILABLE:
        return await m.edit("Search handler is missing.")
    
    url = get_youtube_stream_url(query)
    if not url:
        return await m.edit("Video not found.")
    
    if not VC_AVAILABLE or not call_py:
        return await m.edit("Video found, but Voice Chat module is inactive.")
    
    await m.edit("🎬 Connecting to Voice Chat...")
    
    from vc_handler import start_vc_player
    success = await start_vc_player(call_py, chat_id, url, is_video=True)
    if success:
        await m.edit("▶️ Playing video in VC!")
    else:
        await m.edit("❌ Failed to join Voice Chat.")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    chat_id = message.chat.id
    if call_py:
        try:
            from vc_handler import stop_vc_player
            await stop_vc_player(call_py, chat_id)
        except Exception:
            pass
        await message.reply("⏹ Stopped streaming.")

if __name__ == "__main__":
    app.run()
