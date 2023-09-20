import os

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "6344855563:AAER4AWp7vs2vsWJbVXApq-Pb9stw2uf-C0")
    API_ID = int(os.getenv("API_ID", "14965050"))
    API_HASH = os.getenv("API_HASH", "38bab2dab10fc1b6a9ba0bf683fd7048")
    BOT_OWNER = os.environ.get("BOT_OWNER", "ElikoAndMee")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "ElikoSongBot")
    PLAYLIST_NAME = os.environ.get("PLAYLIST_NAME", "𝙀𝙡𝙞𝙠𝙤 𝙋𝙡𝙖𝙮𝙡𝙞𝙨𝙩")
    PLAYLIST_ID = int(os.environ.get("PLAYLIST_ID", "-1001822732870"))

