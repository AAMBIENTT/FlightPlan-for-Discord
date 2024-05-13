import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_API_CONTEXT = os.getenv("GOOGLE_SHEET_CONTEXT", "")
BITLY_ACCESS_TOKEN = os.getenv("BITLY_ACCESS_TOKEN", "")
GUILD_ID = Server_ID_here
CHANNEL_ID = Channel_ID_here

