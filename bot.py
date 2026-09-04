import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

from yt_handler import get_youtube_stream_url

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

app = Client(
    "sk_bot_v2_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

ass = Client(
    "sk_bot_v2_user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

call_py = PyTgCalls(ass)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply("🎵 **VC Music Bot is Ready!**\nUse `/play <song name>` in group voice chat.")

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Gane ka naam toh likh bhai! Example: `/play Kesariya`")
    
    m = await message.reply("🔍 Searching song...")
    
    url = get_youtube_stream_url(query)
    if not url:
        return await m.edit("Song nahi mila bhai.")
    
    try:
        await m.edit("🎧 Joining Voice Chat...")
        await call_py.join_group_call(
            chat_id,
            MediaStream(url)
        )
        await m.edit(f"▶️ **Playing in VC:** {query}")
    except Exception as e:
        try:
            await call_py.change_stream(chat_id, MediaStream(url))
            await m.edit(f"▶️ **Playing in VC:** {query}")
        except Exception as err:
            await m.edit(f"❌ VC Error: {err}")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    chat_id = message.chat.id
    try:
        await call_py.leave_group_call(chat_id)
        await message.reply("⏹ Stream stopped.")
    except Exception as e:
        await message.reply(f"Error: {e}")

async def main():
    await app.start()
    await ass.start()
    await call_py.start()
    print("-> VC Bot started successfully!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
