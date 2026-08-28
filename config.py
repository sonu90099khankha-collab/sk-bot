import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from pyrogram import Client, filters
import random
from flask import Flask
from threading import Thread
import os
from pytgcalls import PyTgCalls

# Safe import for Audio/Video streams
try:
    from pytgcalls.types import AudioPiped, VideoPiped
except ImportError:
    try:
        from pytgcalls.types.input_stream import AudioPiped, VideoPiped
    except ImportError:
        AudioPiped = None
        VideoPiped = None

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

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

t = Thread(target=run_web)
t.daemon = True
t.start()
