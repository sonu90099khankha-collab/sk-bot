import asyncio
import yt_dlp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from converter import AudioPiped, VideoPiped
import config
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_LINK, CHANNEL_LINK, OWNER_CONTACT

app = Client(
    "VCPlayerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

def get_yt_url(query):
    ydl_opts = {"format": "bestaudio/best", "noplaylist": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            if query.startswith("http"):
                info = ydl.extract_info(query, download=False)
                return info.get("url") or query
            else:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if "entries" in info and info["entries"]:
                    return info["entries"][0].get("url") or info["entries"][0].get("webpage_url")
        except Exception:
            pass
    return None

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    text = (
        "👋 **Music & Video VC Bot is Active!**\n\n"
        "🎵 Play Audio: `/play <song name or link>`\n"
        "📺 Play Video: `/video <video name or link>`\n"
        "⏹️ Stop: `/stop`\n\n"
        f"📢 **Channel:** {CHANNEL_LINK}\n"
        f"👑 **Owner:** {OWNER_CONTACT}\n"
        f"🌐 **Group:** {GROUP_LINK}"
    )
    await message.reply(text, disable_web_page_preview=True)

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name or YouTube link to play!")
    
    m = await message.reply("🔍 Searching on YouTube...")
    try:
        url = get_yt_url(query)
        if not url:
            return await m.edit("❌ Song not found on YouTube!")
        
        await m.edit(f"🎵 Playing audio in VC...")
        await call_py.join_group_call(
            chat_id,
            AudioPiped(url)
        )
    except Exception as e:
        await m.edit(f"Error: {e}")

@app.on_message(filters.command("video"))
async def play_video(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a video name or YouTube link to play!")
    
    m = await message.reply("🔍 Searching video on YouTube...")
    try:
        url = get_yt_url(query)
        if not url:
            return await m.edit("❌ Video not found on YouTube!")
        
        await m.edit(f"📺 Playing video in VC...")
        await call_py.join_group_call(
            chat_id,
            VideoPiped(url)
        )
    except Exception as e:
        await m.edit(f"Error: {e}")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    chat_id = message.chat.id
    try:
        await call_py.leave_group_call(chat_id)
        await message.reply("⏹️ Left the voice chat.")
    except Exception as e:
        await message.reply(f"Error: {e}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app.start()
    call_py.start()
    loop.run_forever()
        
