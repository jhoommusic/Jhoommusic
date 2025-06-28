import os
from os import getenv

# Bot Configuration
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")

# MongoDB Configuration
MONGO_DB_URI = getenv("MONGO_DB_URI", "")

# Music Bot Configuration
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "60"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "180"))

# Pyrogram Configuration
STRING_SESSION = getenv("STRING_SESSION", "")

# Bot Settings
BOT_NAME = getenv("BOT_NAME", "JhoomMusic")
BOT_USERNAME = getenv("BOT_USERNAME", "JhoomMusicBot")

# Owner and Sudo Users
OWNER_ID = list(map(int, getenv("OWNER_ID", "").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))

# Log Configuration
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", ""))

# GitHub Configuration
GITHUB_REPO = getenv("GITHUB_REPO", "")
GIT_TOKEN = getenv("GIT_TOKEN", "")

# Heroku Configuration
HEROKU_API_KEY = getenv("HEROKU_API_KEY", "")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", "")

# Other Configuration
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "")

# Auto Leaving Configuration
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("AUTO_LEAVE_ASSISTANT_TIME", "5400"))

# Spotify Configuration
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "")

# Video Calls Configuration
VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", "3"))
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "30"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))

# Images
START_IMG_URL = getenv("START_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
GLOBAL_IMG_URL = getenv("GLOBAL_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://telegra.ph/file/56d1760224589ee370186.jpg")