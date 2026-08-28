import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioStream, VideoStream
from flask import Flask
from threading import Thread

# Event loop fix
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

CHANNEL_LINK = "https://t.me/Love_Angels_10"
OWNER_CONTACT = "https://t.me/Love_Angels_10"
GROUP_LINK = "https://t.me/Love_Angels_10"

app = Client(
    "VCPlayerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

# Aliases for bot.py compatibility
AudioPiped = AudioStream
VideoPiped = VideoStream

# Flask web server to keep Render alive
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# Run Flask in background thread
t = Thread(target=run_web)
t.daemon = True
t.start()
