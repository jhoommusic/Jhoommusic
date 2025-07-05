import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# MongoDB Configuration
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")

# Music Bot Configuration
DURATION_LIMIT_MIN = int(os.getenv("DURATION_LIMIT", "60"))
SONG_DOWNLOAD_DURATION = int(os.getenv("SONG_DOWNLOAD_DURATION", "180"))

# Pyrogram Configuration
STRING_SESSION = os.getenv("STRING_SESSION", "")

# Bot Settings
BOT_NAME = os.getenv("BOT_NAME", "JhoomMusic")
BOT_USERNAME = os.getenv("BOT_USERNAME", "JhoomMusicBot")

# Owner and Sudo Users
OWNER_ID = list(map(int, os.getenv("OWNER_ID", "").split())) if os.getenv("OWNER_ID") else []
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "").split())) if os.getenv("SUDO_USERS") else []

# Log Configuration
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0")) if os.getenv("LOG_GROUP_ID") else None

# GitHub Configuration
GITHUB_REPO = os.getenv("GITHUB_REPO", "")
GIT_TOKEN = os.getenv("GIT_TOKEN", "")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")

# Heroku Configuration
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "")
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "")

# Other Configuration
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/JhoomMusicSupport")
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/JhoomMusicChannel")

# Auto Leaving Configuration
AUTO_LEAVING_ASSISTANT = os.getenv("AUTO_LEAVING_ASSISTANT", "True").lower() == "true"
AUTO_LEAVE_ASSISTANT_TIME = int(os.getenv("AUTO_LEAVE_ASSISTANT_TIME", "5400"))

# Spotify Configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

# Video Calls Configuration
VIDEO_STREAM_LIMIT = int(os.getenv("VIDEO_STREAM_LIMIT", "3"))
SERVER_PLAYLIST_LIMIT = int(os.getenv("SERVER_PLAYLIST_LIMIT", "30"))
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", "25"))

# Images
START_IMG_URL = os.getenv("START_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
PING_IMG_URL = os.getenv("PING_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
PLAYLIST_IMG_URL = os.getenv("PLAYLIST_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
GLOBAL_IMG_URL = os.getenv("GLOBAL_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
STATS_IMG_URL = os.getenv("STATS_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
TELEGRAM_AUDIO_URL = os.getenv("TELEGRAM_AUDIO_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
TELEGRAM_VIDEO_URL = os.getenv("TELEGRAM_VIDEO_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
STREAM_IMG_URL = os.getenv("STREAM_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
SOUNCLOUD_IMG_URL = os.getenv("SOUNCLOUD_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
YOUTUBE_IMG_URL = os.getenv("YOUTUBE_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
SPOTIFY_ARTIST_IMG_URL = os.getenv("SPOTIFY_ARTIST_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
SPOTIFY_ALBUM_IMG_URL = os.getenv("SPOTIFY_ALBUM_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
SPOTIFY_PLAYLIST_IMG_URL = os.getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")

# Additional Configuration
BANNED_USERS = []
CLEANMODE_DELETE_MINS = int(os.getenv("CLEANMODE_DELETE_MINS", "5"))

# Cache Configuration
CACHE_DIR = "cache"
DOWNLOAD_DIR = "downloads"
RAW_FILES_DIR = "raw_files"

# FFmpeg Configuration
FFMPEG_PROCESSES = int(os.getenv("FFMPEG_PROCESSES", "2"))

# Redis Configuration (Optional)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# Auto Update Configuration
AUTO_UPDATE = os.getenv("AUTO_UPDATE", "True").lower() == "true"
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "")

# Validation
if not API_ID or not API_HASH or not BOT_TOKEN:
    print("❌ Missing required environment variables: API_ID, API_HASH, BOT_TOKEN")
    exit(1)

if not STRING_SESSION:
    print("⚠️ STRING_SESSION not found, userbot will be disabled")

print("✅ Configuration loaded successfully")
print(f"✅ API_ID: {API_ID}")
print(f"✅ BOT_NAME: {BOT_NAME}")
print(f"✅ STRING_SESSION: {'Found' if STRING_SESSION else 'Not Found'}")
