from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

def setup_calls(app):
    return PyTgCalls(app)

async def play_audio_stream(call_py, chat_id, url):
    try:
        await call_py.join_group_call(
            chat_id,
            MediaStream(
                url,
                stream_type=MediaStream.Audio
            )
        )
    except Exception:
        pass

async def stop_stream(call_py, chat_id):
    try:
        await call_py.leave_group_call(chat_id)
    except Exception:
        pass
        
