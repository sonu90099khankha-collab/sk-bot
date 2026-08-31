from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, VideoPiped

def setup_calls(app):
    return PyTgCalls(app)

async def play_audio_stream(call_py, chat_id, url):
    await call_py.join_group_call(
        chat_id,
        AudioPiped(url)
    )

async def play_video_stream(call_py, chat_id, url):
    await call_py.join_group_call(
        chat_id,
        VideoPiped(url)
    )

async def stop_stream(call_py, chat_id):
    await call_py.leave_group_call(chat_id)
        
