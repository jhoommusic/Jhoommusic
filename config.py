import os
getenv = os.getenv
import os
from dotenv import load_dotenv
load_dotenv()
DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "60"))
DURATION_LIMIT_MIN = int(DURATION_LIMIT // 60)
PING_IMG_URL = os.getenv("PING_IMG_URL", "https://telegra.ph/file/68e5f6e5b3d5c719b634d.jpg")
BANNED_USERS = set()
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/JhoomMusicChannel")
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/JhoomMusicChannel")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/JhoomMusicSupport")
Support_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/JhoomMusicSupport")
BOT_NAME = os.getenv("BOT_NAME", "JhoomMusic")
BOT_NAME = os.getenv("BOT_NAME", "JhoomMusic")
START_IMG_URL = os.getenv("START_IMG_URL", "https://telegra.ph/file/68e5f6e5b3d5c719b634d.jpg")
load_dotenv()
DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "60"))
DURATION_LIMIT_MIN = int(DURATION_LIMIT // 60)
PING_IMG_URL = os.getenv("PING_IMG_URL", "https://telegra.ph/file/68e5f6e5b3d5c719b634d.jpg")
BANNED_USERS = set()
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/JhoomMusicChannel")
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/JhoomMusicChannel")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/JhoomMusicSupport")
Support_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/JhoomMusicSupport")
BOT_NAME = os.getenv("BOT_NAME", "JhoomMusic")
BOT_NAME = os.getenv("BOT_NAME", "JhoomMusic")
START_IMG_URL = os.getenv("START_IMG_URL", "https://telegra.ph/file/68e5f6e5b3d5c719b634d.jpg")
from pyrogram import Client

api_id = 123456
api_hash = 'your_api_hash_here'
session_name = 'jhoom_bot'

app = Client(session_name, api_id=api_id, api_hash=api_hash)
userbot = None


# Owner and Sudo Config
OWNER_ID = [123456789]
SUDO_USERS = [123456789]

# Required API Credentials
API_ID = 123456
API_HASH = 'your_api_hash_here'
BOT_TOKEN = 'your_bot_token_here'

# Optional String Session
STRING_SESSION = None

# GitHub Repo Link
GITHUB_REPO = 'https://github.com/jhoommusic/Jhoommusic'

# GitHub Token (optional, for public repo keep it blank)
GIT_TOKEN = ''

# Heroku Config (optional)
HEROKU_API_KEY = ''
HEROKU_APP_NAME = ''

# Banned Users List
BANNED_USERS = []

# Bot Username
BOT_USERNAME = 'your_bot_username_here'
DURATION_LIMIT_MIN = int(getenv('DURATION_LIMIT', '60'))

# Additional Configs
PING_IMG_URL = getenv("PING_IMG_URL", "https://telegra.ph/file/60752df1ea8f6d24909f7.jpg")
START_IMG_URL = getenv("START_IMG_URL", "https://telegra.ph/file/60752df1ea8f6d24909f7.jpg")
BOT_NAME = getenv("BOT_NAME", "JhoomMusic")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/JhoomMusicSupport")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/JhoomMusicChannel")
