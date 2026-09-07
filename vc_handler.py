import os
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, VideoPiped
from pyrogram import Client

def setup_vc_calls(app):
    try:
        string_session = os.getenv("STRING_SESSION", "")
        if string_session:
            assistant = Client(
                "assistant",
                api_id=int(os.getenv("API_ID", "0")),
                api_hash=os.getenv("API_HASH", ""),
                session_string=string_session
            )
            call_py = PyTgCalls(assistant)
        else:
            call_py = PyTgCalls(app)
            
        return call_py
    except Exception as e:
        print(f"PyTgCalls Setup Error: {e}")
        return None

async def start_vc_player(call_py, chat_id, url, is_video=False):
    if not call_py:
        return False
    try:
        if not call_py.is_connected:
            await call_py.start()

        if is_video:
            await call_py.join_group_call(chat_id, VideoPiped(url))
        else:
            await call_py.join_group_call(chat_id, AudioPiped(url))
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
        
