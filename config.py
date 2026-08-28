import os
import asyncio

# Event loop fix for async operations
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from pyrogram import Client, filters
from pytgcalls import PyTgCalls

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
