import os

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

GROUP_LINK = os.environ.get("GROUP_LINK", "https://t.me/your_group")
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/your_channel")
OWNER_CONTACT = os.environ.get("OWNER_CONTACT", "@your_username")
STRING_SESSION = os.getenv("STRING_SESSION", "")
