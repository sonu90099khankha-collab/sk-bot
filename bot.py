import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from pyrogram import Client, filters

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

# Official Bot Client for handling telegram commands
app = Client(
    "sk_bot_v2_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Assistant Client for joining voice chats
ass = Client(
    "sk_bot_v2_user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

call_py = None
if VC_AVAILABLE:
    try:
        call_py = PyTgCalls(ass)
        print("-> PyTgCalls client initialized successfully!")
    except Exception as e:
        print(f"-> PyTgCalls client init failed: {e}")
        call_py = None
        VC_AVAILABLE = False

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    text = (
        "🎵 **Audio/Video VC Bot is Live!**\n\n"
        "• Use `/play <song name>` for audio.\n"
        "• Use `/vplay <song name>` for video."
    )
    await message.reply(text)

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name! Example: `/play Stay`")
    
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
        try:
            await call_py.change_stream(chat_id, AudioPiped(url))
            await m.edit("▶️ Playing audio in VC!")
        except Exception as err:
            await m.edit(f"❌ Failed to join VC: {err}")

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
    
    await m.edit("🎬 Joining Voice Chat...")
    
    try:
        await call_py.join_group_call(
            chat_id,
            VideoPiped(url)
        )
        await m.edit("▶️ Playing video in VC!")
    except Exception as e:
        print(f"VPlay Error: {e}")
        try:
            await call_py.change_stream(chat_id, VideoPiped(url))
            await m.edit("▶️ Playing video in VC!")
        except Exception as err:
            await m.edit(f"❌ Failed to join VC: {err}")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    chat_id = message.chat.id
    if call_py:
        try:
            await call_py.leave_group_call(chat_id)
        except Exception:
            pass
     await message.reply("⏹ Stream stopped.")

import asyncio

async def main():
    await app.start()
    await ass.start()
    if call_py:
        await call_py.start()
    print("-> Bot and Assistant started successfully!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(main())
