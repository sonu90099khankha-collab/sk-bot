from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, VideoPiped

def setup_vc_calls(app):
    try:
        call_py = PyTgCalls(app)
        call_py.start()
        return call_py
    except Exception as e:
        print(f"PyTgCalls Setup Error: {e}")
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
    except Exception as e:
        print(f"VC Play Error: {e}")
        return False

async def stop_vc_player(call_py, chat_id):
    if not call_py:
        return
    try:
        await call_py.leave_group_call(chat_id)
    except Exception:
        pass
      
