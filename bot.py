import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from pyrogram import Client, filters

# PyTgCalls Import & Setup
try:
    from pytgcalls import PyTgCalls
    from pytgcalls.types import AudioPiped, VideoPiped
    VC_AVAILABLE = True
    print("-> PyTgCalls library loaded successfully.")
except Exception as e:
    print(f"-> PyTgCalls load error: {e}")
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
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")

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
        call_py = PyTgCalls(app)
        print("-> PyTgCalls client initialized successfully!")
    except Exception as e:
        print(f"-> PyTgCalls client init failed: {e}")
        call_py = None
        VC_AVAILABLE = False

@app.on_message(filters.command(["start", "help"]))
async def start_cmd(client, message):
    text = (
        "🎵 **Audio/Video VC Bot is Live!**\n\n"
        "• Audio commands: `/play`, `/ple`, `/ppp`, `/p` <song name>\n"
        "• Video commands: `/vplay`, `/vp`, `/vppp` <video name>"
    )
    await message.reply(text)

# Yahan humne play ke alawa ppp, ple, p sab jod diya hai taaki typo hone par bhi chale
@app.on_message(filters.command(["play", "ple", "ppp", "p"]))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name! Example: `/ppp गोविंद song`")
    
    m = await message.reply("🔍 Searching song...")
    
    if not YT_AVAILABLE:
        return await m.edit("Search handler is missing.")
    
    url = get_youtube_stream_url(query)
    if not url:
        return await m.edit("Song not found.")
    
    if not VC_AVAILABLE or not call_py:
        return await m.edit("Song found, but Voice Chat module is inactive.")
    
    await m.edit("🎧 Joining Voice Chat...")
    
    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped(url)
        )
        await m.edit("▶️ Playing audio in VC!")
    except Exception as e:
        print(f"Play Error: {e}")
        await m.edit(f"❌ Failed to join VC: {e}")

# Yahan video play ke liye bhi shortcuts jod diye hain
@app.on_message(filters.command(["vplay", "vple", "vppp", "vp"]))
async def play_video(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a video name! Example: `/vppp गोविंद song`")
    
    m = await message.reply("🔍 Searching video...")
    
    if not YT_AVAILABLE:
        return await m.edit("Search handler is missing.")
    
    url = get_youtube_stream_url(query)
    if not url:
        return await m.edit("Video not found.")
    
    if not VC_AVAILABLE or not call_py:
        return await m.edit("Video found, but Voice Chat module is inactive.")
    
    await m.edit("🎬 Joining Voice Chat...")
    
    try:
        await call_py.join_group_call(
            chat_id,
            VideoPiped(url)
        )
        await m.edit("▶️ Playing video in VC!")
    except Exception as e:
        print(f"VPlay Error: {e}")
        await m.edit(f"❌ Failed to join VC: {e}")

@app.on_message(filters.command(["stop", "end", "leave"]))
async def stop_call(client, message):
    chat_id = message.chat.id
    if call_py:
        try:
            await call_py.leave_group_call(chat_id)
        except Exception:
            pass
        await message.reply("⏹ Stream stopped.")

if __name__ == "__main__":
    app.run()
