import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import yt_dlp

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("sk_music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Contact Owner", url="https://t.me/SK_KING_CHILL")]
    ])
    await message.reply(
        "🎵 **Welcome to SK Music Bot!**\n\n"
        "Add me to your group, turn on video chat, and type:\n"
        "`/play [song name]` to play music.\n\n"
        "To contact the owner, click below:",
        reply_markup=keyboard
    )

@app.on_message(~filters.me & filters.private & ~filters.command(["start", "play", "stop"]))
async def forward_to_owner(client, message):
    try:
        await message.forward(chat_id="SK_KING_CHILL")
        await message.reply("✅ Your message has been sent to the Owner (@SK_KING_CHILL). They will reply soon!")
    except Exception as e:
        print(f"Forward error: {e}")

@app.on_message(filters.command("play"))
async def play_media(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ Please provide a song name, e.g., `/play kesariya`")
        return
        
    query = " ".join(message.command[1:])
    m = await message.reply("🔍 Searching on YouTube...")
    
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "default_search": "ytsearch",
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if "entries" in info and len(info["entries"]) > 0:
                media_info = info["entries"][0]
                url = media_info["url"]
                title = media_info.get("title", "Unknown")
            else:
                await m.edit("❌ Media not found!")
                return
                
        chat_id = message.chat.id
        await call_py.join_group_call(
            chat_id,
            AudioPiped(url)
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Contact Owner", url="https://t.me/SK_KING_CHILL")]
        ])
        
        await m.edit(f"▶️ **Now Playing:** {title}", reply_markup=keyboard)
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")

@app.on_message(filters.command("stop"))
async def stop_media(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply("⏹️ Stream stopped.")
    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")

async def main():
    await app.start()
    await call_py.start()
    print("Bot started successfully!")
    await asyncio.gather(asyncio.Event().wait())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
