from dotenv import load_dotenv
load_dotenv()

import os
from os import getenv

# Bot Configuration
API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")

# MongoDB Configuration (Safe import)
MONGO_DB_URI = getenv("MONGO_DB_URI", "disabled")
mongodb = None
if MONGO_DB_URI != "disabled":
    try:
        from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
        mongodb = MongoClient(MONGO_DB_URI).jhoommusic
    except ImportError:
        mongodb = None

# Music Bot Configuration
OWNER_ID = int(getenv("OWNER_ID", 0))
STRING_SESSION = getenv("STRING_SESSION", "")
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "")
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0))
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "JhoomMusic")
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT_MIN", 180))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
