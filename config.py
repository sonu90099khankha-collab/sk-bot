import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioStream, VideoStream

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
