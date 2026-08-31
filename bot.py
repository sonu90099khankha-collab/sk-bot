import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import yt_dlp
from pyrogram import Client, filters

# Safely import VC handler so that even if it fails, the main bot stays alive
try:
    from vc_handler import setup_vc_calls, start_vc_player, stop_vc_player
    VC_AVAILABLE = True
except Exception:
    VC_AVAILABLE = False

# Render keep-alive web server
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

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

call_py = None
if VC_AVAILABLE:
    try:
        call_py = setup_vc_calls(app)
    except Exception:
        call_py = None

def get_yt_url(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in info:
                info = info['entries'][0]
            return info['url']
        except Exception:
            return None

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    text = (
        "🎵 **Audio/Video VC Bot is Live!**\n\n"
        "• **Group Link:** [Join Group](https://t.me/+ZJDUfVhCpco1ZDA1)\n"
        "• **Owner DM:** [@SK_KING_CHILL](https://t.me/SK_KING_CHILL)\n\n"
        "• Use `/play <song name>` for audio\n"
        "• Use `/vplay <song name>` for video"
    )
    await message.reply(text, disable_web_page_preview=True)

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name! Example: `/play fading`")

    m = await message.reply("🔍 Searching for the song...")
    url = get_yt_url(query)
    if not url:
        return await m.edit("Song not found!")

    if not VC_AVAILABLE or not call_py:
        return await m.edit("▶️ Song found, but Voice Chat module is inactive.")

    await m.edit("🎧 Connecting to Voice Chat...")
    success = await start_vc_player(call_py, chat_id, url, is_video=False)
    if success:
        await m.edit("▶️ Playing audio in Voice Chat!")
    else:
        await m.edit("❌ Failed to join Voice Chat, but bot is safe and running!")

@app.on_message(filters.command("vplay"))
async def play_video(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a video name! Example: `/vplay fading`")

    m = await message.reply("🔍 Searching for the video...")
    url = get_yt_url(query)
    if not url:
        return await m.edit("Video not found!")

    if not VC_AVAILABLE or not call_py:
        return await m.edit("▶️ Video found, but Voice Chat module is inactive.")

    await m.edit("🎥 Connecting to Voice Chat for Video...")
    success = await start_vc_player(call_py, chat_id, url, is_video=True)
    if success:
        await m.edit("🎬 Playing video in Voice Chat!")
    else:
        await m.edit("❌ Failed to stream video, but bot is safe and running!")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    chat_id = message.chat.id
    if call_py:
        try:
            await stop_vc_player(call_py, chat_id)
        except Exception:
            pass
    await message.reply("⏹️ Stopped streaming.")

if __name__ == "__main__":
    app.run()
    
