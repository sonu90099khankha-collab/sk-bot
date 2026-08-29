import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import VideoPiped
import yt_dlp

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("sk_music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply("🎥 **SK-Bot Video/Audio Bot is Online!**\n\nTurn on the video chat in your group and type:\n`/play [song name]`\n\nTo stop, type:\n`/stop`")

@app.on_message(filters.command("play"))
async def play_media(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ Please provide a video/song name, for example: `/play kesariya`")
        return
        
    query = " ".join(message.command[1:])
    m = await message.reply("🔍 Searching on YouTube...")
    
    ydl_opts = {
        "format": "best",
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
                await m.edit("❌ Video not found!")
                return
                
        chat_id = message.chat.id
        await call_py.join_group_call(
            chat_id,
            VideoPiped(url)
        )
        await m.edit(f"▶️ **Now Streaming (Video + Audio):** {title}")
    except Exception as e:
        await m.edit(f"❌ An error occurred: `{e}`")

@app.on_message(filters.command("stop"))
async def stop_media(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply("⏹️ Stream has been stopped.")
    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")

call_py.start()
app.run()
