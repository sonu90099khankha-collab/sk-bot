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

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped

# Flask server to keep Render alive 24/7
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Credentials
API_ID = 5239609996
API_HASH = "b18441a1ff607e10a989891a54620000"
BOT_TOKEN = "7595641951:AAGJ1bJUdX_Bl0p_Wfv8u6fWctnALGUnVTQ"

GROUP_LINK = "https://t.me/SK_Chatting_Club"
OWNER_DM = "https://t.me/S_K_KI_NG"

app = Client(
    "MusicBotSession",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Join Group", url=GROUP_LINK),
            InlineKeyboardButton("Contact Owner", url=OWNER_DM)
        ]
    ])
    
    await message.reply_text(
        "Hello! Your Music Bot is now online and ready.\n"
        "Use /play [song name or link] to play music in Voice Chat.\n\n"
        "Click the buttons below to join our group or contact the owner:",
        reply_markup=keyboard
    )

@app.on_message(filters.command("play"))
async def play_music(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply_text("Please provide a song name or link. Example: `/play Naatu Naatu`")
        return
    
    query = message.text.split(None, 1)[1]
    await message.reply_text(f"Searching and connecting to Voice Chat for: **{query}**...")
    
    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        )
        await message.reply_text("Music is now playing successfully in the Voice Chat!")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

async def main():
    t = Thread(target=run_flask)
    t.start()
    
    await app.start()
    await call_py.start()
    print("Music Bot successfully started with Flask server!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
    
