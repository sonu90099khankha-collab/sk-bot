try:
    from pytgcalls.types import AudioPiped, VideoPiped
except ImportError:
    try:
        from pytgcalls.types.input_stream import AudioPiped, VideoPiped
    except ImportError:
        AudioPiped = None
        VideoPiped = None

import sys
from pyrogram import errors
if not hasattr(errors, "GroupcallForbidden"):
    class GroupcallForbidden(Exception):
        pass
    errors.GroupcallForbidden = GroupcallForbidden
    
