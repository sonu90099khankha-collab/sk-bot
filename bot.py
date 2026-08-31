import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import yt_dlp
from pyrogram import Client, filters
from stream_helper import setup_calls, play_audio_stream, stop_stream

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
call_py = setup_calls(app)

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
        "🎵 **Audio VC Bot is Live!**\n\n"
        "• **Group Link:** [Join Group](https://t.me/+ZJDUfVhCpco1ZDA1)\n"
        "• **Owner DM:** [@SK_KING_CHILL](https://t.me/SK_KING_CHILL)\n\n"
        "Use `/play <song name>` to play music in Voice Chat."
    )
    await message.reply(text, disable_web_page_preview=True)

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name! Example: `/play fading`")

    m = await message.reply("🔍 Searching for the song...")
    try:
        url = get_yt_url(query)
        if not url:
            return await m.edit("Song not found!")

        await m.edit("🎧 Connecting to Voice Chat...")
        await play_audio_stream(call_py, chat_id, url)
        await m.edit("▶️ Playing audio in Voice Chat!")
    except Exception as e:
        await m.edit(f"An error occurred: {e}")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    chat_id = message.chat.id
    try:
        await stop_stream(call_py, chat_id)
        await message.reply("⏹️ Stopped streaming and left the Voice Chat.")
    except Exception as e:
        await message.reply(f"Error: {e}")

async def main():
    await app.start()
    await call_py.start()
    await asyncio.gather(asyncio.Event().wait())

if __name__ == "__main__":
    asyncio.run(main())
                         
