# Safe import for Audio/Video streams
try:
    from pytgcalls.types import AudioPiped, VideoPiped
except ImportError:
    try:
        from pytgcalls.types.input_stream import AudioPiped, VideoPiped
    except ImportError:
        AudioPiped = None
        VideoPiped = None

# Dummy fix for GroupcallForbidden error in py-tgcalls
import sys
from pyrogram import errors
if not hasattr(errors, "GroupcallForbidden"):
    class GroupcallForbidden(Exception):
        pass
    errors.GroupcallForbidden = GroupcallForbidden
