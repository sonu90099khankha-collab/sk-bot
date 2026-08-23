import asyncio
import os
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import VideoPiped
import yt_dlp

# Safe Event Loop Setup for Python
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Flask Server to keep Render alive 24/7
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Music Video Bot is online and running!"

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Credentials (Loaded securely from Render Environment Variables)
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

GROUP_LINK = "https://t.me/SK_Chatting_Club"
OWNER_DM = "https://t.me/S_K_KI_NG"

# यहाँ अपनी फोटो की डायरेक्ट Raw लिंक डालें (जो गिटहब में अपलोड होगी)
USER_DP_URL = "https://raw.githubusercontent.com/sonu90099khankha-collab/sk-bot/main/my_photo.jpg"

# Initialize Pyrogram Client and PyTgCalls
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
        "👋 Hello! Video DP Music Bot is Online!\n\n"
        "• Use `/play [song name]` in group voice chat to play music with your photo DP.\n"
        "• Use `/stop` to stop the music.",
        reply_markup=keyboard
    )

@app.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a song name! Example: `/play Tum Hi Ho`")
    
    query = " ".join(message.command[1:])
    m = await message.reply_text(f"🔍 Searching for: `{query}`...")

    try:
        ydl_opts = {'format': 'bestaudio', 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in info:
                info = info['entries'][0]
            audio_url = info['url']
            title = info['title']

        # Joining Voice Chat with Audio and User Photo (VideoPiped)
        await call_py.join_group_call(
            message.chat.id,
            VideoPiped(
                audio_source=audio_url,
                video_source=USER_DP_URL
            )
        )
        await m.edit(f"🎵 Now Playing: `{title}`\n🖼 DP Stream Active\n👤 Requested by: {message.from_user.mention}")
    
    except Exception as e:
        await m.edit(f"❌ Error occurred: `{e}`")

@app.on_message(filters.command("stop") & filters.group)
async def stop_music(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("⏹ Music stopped and bot left the voice chat.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

async def main():
    # Start Flask server in background thread
    t = Thread(target=run_flask)
    t.start()
    
    await app.start()
    await call_py.start()
    print("🚀 Music Bot with Video DP started successfully!")
    await asyncio.gather(*(asyncio.Event().wait(),))

if __name__ == "__main__":
    loop.run_until_complete(main())
