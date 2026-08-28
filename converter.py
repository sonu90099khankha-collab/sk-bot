# Safe import for Audio/Video streams
try:
    from pytgcalls.types import AudioPiped, VideoPiped
except ImportError:
    try:
        from pytgcalls.types.input_stream import AudioPiped, VideoPiped
    except ImportError:
        AudioPiped = None
        VideoPiped = None
      
