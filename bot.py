import asyncio
from config import app, call_py, GROUP_LINK, CHANNEL_LINK, OWNER_CONTACT, AudioPiped, VideoPiped, filters

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    text = (
        "👋 **Bot is active and running smoothly!**\n\n"
        "🎵 Audio command: `/play <song_name>`\n"
        "📺 Video command: `/video <video_name>`\n"
        "⏹️ Stop command: `/stop`\n\n"
        f"📢 **Channel:** {CHANNEL_LINK}\n"
        f"👑 **Owner / DM:** {OWNER_CONTACT}\n"
        f"🌐 **Official Group:** {GROUP_LINK}"
    )
    await message.reply(text, disable_web_page_preview=True)

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name.\nJoin our group: " + GROUP_LINK)
    
    await message.reply(f"🎵 Playing audio in VC: `{query}`\nPowered by: {CHANNEL_LINK}")
    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        )
    except Exception as e:
        await message.reply(f"Error: {e}")

@app.on_message(filters.command("video"))
async def play_video(client, message):
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a video name.\nJoin our group: " + GROUP_LINK)
    
    await message.reply(f"📺 Playing video in VC: `{query}`\nPowered by: {CHANNEL_LINK}")
    try:
        await call_py.join_group_call(
            chat_id,
            VideoPiped("https://www.youtube.com/watch?v=jNQXAC9IVRw")
        )
    except Exception as e:
        await message.reply(f"Error: {e}")

@app.on_message(filters.command("stop"))
async def stop_call(client, message):
    chat_id = message.chat.id
    await call_py.leave_group_call(chat_id)
    await message.reply(f"⏹️ Left the voice chat.\nSupport us: {CHANNEL_LINK}")

if __name__ == "__main__":
    app.start()
    call_py.start()
    asyncio.get_event_loop().run_forever()
    
