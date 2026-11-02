import os
from dotenv import load_dotenv

load_dotenv()

# ====================== REQUIRED ======================
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING_SESSION = os.getenv("STRING_SESSION", None)

# ====================== OWNER / SUDO ==================
OWNER_ID = [int(x) for x in os.getenv("OWNER_ID", "0").split() if x.isdigit()]
SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split() if x.isdigit()]

# ====================== BOT SETTINGS ==================
BOT_NAME = os.getenv("BOT_NAME", "JhoomMusic")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))

# ====================== SUPPORT =======================
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/JhoomMusicSupport")
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/JhoomMusicChannel")

# ====================== MUSIC LIMITS ==================
DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "60"))          # minutes
DURATION_LIMIT_MIN = DURATION_LIMIT
SONG_DOWNLOAD_DURATION = int(os.getenv("SONG_DOWNLOAD_DURATION", "180"))
VIDEO_STREAM_LIMIT = int(os.getenv("VIDEO_STREAM_LIMIT", "3"))
SERVER_PLAYLIST_LIMIT = int(os.getenv("SERVER_PLAYLIST_LIMIT", "30"))
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", "25"))

# ====================== AUTO LEAVE ====================
AUTO_LEAVING_ASSISTANT = os.getenv("AUTO_LEAVING_ASSISTANT", "True").lower() == "true"
AUTO_LEAVE_ASSISTANT_TIME = int(os.getenv("AUTO_LEAVE_ASSISTANT_TIME", "5400"))

# ====================== DATABASE ======================
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")

# ====================== OPTIONAL ======================
GITHUB_REPO = os.getenv("GITHUB_REPO", "https://github.com/jhoommusic/Jhoommusic")
GIT_TOKEN = os.getenv("GIT_TOKEN", "")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "")
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "")

# ====================== IMAGES ========================
PING_IMG_URL = os.getenv("PING_IMG_URL", "https://telegra.ph/file/60752df1ea8f6d24909f7.jpg")
START_IMG_URL = os.getenv("START_IMG_URL", "https://telegra.ph/file/60752df1ea8f6d24909f7.jpg")

# ====================== RUNTIME =======================
BANNED_USERS = []
