import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_handler import get_youtube_stream_url

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SESSION_STRING = os.environ.get("SESSION_STRING")

if SESSION_STRING:
    app = Client("music_bot", api_id=int(API_ID), api_hash=API_HASH, session_string=SESSION_STRING)
else:
    app = Client("music_bot", api_id=int(API_ID), api_hash=API_HASH, bot_token=BOT_TOKEN)

pytgcalls = PyTgCalls(app)

@app.on_message(filters.command("play"))
async def heavy_play_handler(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("❌ Please provide a song name! Example: `/play Kesariya`")
        return
        
    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    
    status_msg = await message.reply("🔍 Searching song...")
    
    try:
        stream_url = get_youtube_stream_url(query)
        
        if not stream_url:
            await status_msg.edit("❌ Song not found. Try a different name.")
            return
            
        try:
            await pytgcalls.join_group_call(
                chat_id,
                AudioPiped(stream_url)
            )
        except Exception:
            await pytgcalls.change_stream(
                chat_id,
                AudioPiped(stream_url)
            )
        
        await status_msg.edit(f"🎵 **Playing Now:** `{query}`")
        
    except Exception as e:
        await status_msg.edit(f"❌ Error: {str(e)}")

@app.on_message(filters.command("stop"))
async def stop_handler(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        await message.reply("⏹️ Music stopped and left VC.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

async def main():
    print("🚀 Starting Music Bot...")
    await app.start()
    try:
        await pytgcalls.start()
    except Exception as e:
        print(f"PyTgCalls start warning: {e}")
    await asyncio.Future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
