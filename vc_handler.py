from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, VideoPiped

def setup_vc_calls(app):
    try:
        call_py = PyTgCalls(app)
        return call_py
    except Exception:
        return None

async def start_vc_player(call_py, chat_id, url, is_video=False):
    if not call_py:
        return False
    try:
        if is_video:
            await call_py.join_group_call(
                chat_id,
                VideoPiped(url)
            )
        else:
            await call_py.join_group_call(
                chat_id,
                AudioPiped(url)
            )
        return True
    except Exception:
        return False

async def stop_vc_player(call_py, chat_id):
    if not call_py:
        return
    try:
        await call_py.leave_group_call(chat_id)
    except Exception:
        pass
                          
