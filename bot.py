import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import yt_dlp
from pyrogram import Client, filters

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
        "Use `/play <song name>` to play music."
    )
    await message.reply(text, disable_web_page_preview=True)

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name! Example: `/play fading`")

    m = await message.reply("🔍 Searching for the song...")
    try:
        url = get_yt_url(query)
        if not url:
            return await m.edit("Song not found!")

        await m.edit(f"✅ Song found! Ready to play.")
    except Exception as e:
        await m.edit(f"An error occurred: {e}")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    await message.reply("⏹️ Stopped.")

if __name__ == "__main__":
    app.run()
    
