import os
import time
import asyncio
import yt_dlp
import spotipy
import platform
import psutil
import pyrogram
from spotipy.oauth2 import SpotifyClientCredentials
import logging
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
    InputMediaPhoto
)
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import random
import textwrap
import ffmpeg
import hashlib
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
import concurrent.futures
import signal
from collections import defaultdict
from logging.handlers import RotatingFileHandler
import json
import redis
import aiohttp
from pytgcalls.exceptions import NoActiveGroupCall

# ======================
# CONFIGURATION
# ======================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'jhoommusic.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate required environment variables
required_env_vars = [
    "API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URI", 
    "SUPER_GROUP_ID", "SUPER_GROUP_USERNAME"
]
missing = [var for var in required_env_vars if not os.getenv(var)]
if missing:
    logger.error(f"Missing required environment variables: {', '.join(missing)}")
    exit(1)

# Configuration
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split(",") if x]
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
BOT_IMAGE = "https://i.imgur.com/1StRoLJ.png"
FFMPEG_PROCESSES = int(os.getenv("FFMPEG_PROCESSES", "4"))
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
SUPER_GROUP_ID = int(os.getenv("SUPER_GROUP_ID"))
SUPER_GROUP_USERNAME = os.getenv("SUPER_GROUP_USERNAME")
MAX_PLAYLIST_SIZE = 100
MAX_QUEUE_SIZE = 50
MAX_HISTORY_SIZE = 20
MAX_THUMBNAIL_CACHE = 100

# UI Images
UI_IMAGES = {
    "main_menu": "https://i.imgur.com/JhoomMainMenu.jpg",
    "commands_menu": "https://i.imgur.com/JhoomCommands.jpg",
    "playlist": "https://i.imgur.com/JhoomPlaylist.jpg",
    "diagnostics": "https://i.imgur.com/JhoomDiagnostics.jpg",
    "admin": "https://i.imgur.com/JhoomAdmin.jpg",
    "error": "https://i.imgur.com/JhoomError.jpg",
    "success": "https://i.imgur.com/JhoomSuccess.jpg",
    "player": "https://i.imgur.com/JhoomPlayer.jpg",
    "radio": "https://i.imgur.com/JhoomRadio.jpg",
    "settings": "https://i.imgur.com/JhoomSettings.jpg",
    "volume": "https://i.imgur.com/JhoomVolume.jpg",
    "quality": "https://i.imgur.com/JhoomQuality.jpg",
    "language": "https://i.imgur.com/JhoomLanguage.jpg",
    "notifications": "https://i.imgur.com/JhoomNotifications.jpg",
    "channel": "https://i.imgur.com/JhoomChannel.jpg",
    "speed": "https://i.imgur.com/JhoomSpeed.jpg",
    "download": "https://i.imgur.com/JhoomDownload.jpg",
    "loop": "https://i.imgur.com/JhoomLoop.jpg",
    "shuffle": "https://i.imgur.com/JhoomShuffle.jpg",
    "seek": "https://i.imgur.com/JhoomSeek.jpg",
    "broadcast": "https://i.imgur.com/JhoomBroadcast.jpg",
    "startup": "https://i.imgur.com/JhoomStartup.jpg",
    "queue": "https://i.imgur.com/JhoomQueue.jpg",
    "block": "https://i.imgur.com/JhoomBlock.jpg",
    "blacklist": "https://i.imgur.com/JhoomBlacklist.jpg",
    "gbans": "https://i.imgur.com/JhoomGBans.jpg",
    "license": "https://i.imgur.com/JhoomLicense.jpg",
    "revamp": "https://i.imgur.com/JhoomRevamp.jpg",
    "sultan": "https://i.imgur.com/JhoomSultan.jpg",
    "spiral": "https://i.imgur.com/JhoomSpiral.jpg"
}

# Thread pool for background tasks
executor = concurrent.futures.ThreadPoolExecutor(max_workers=FFMPEG_PROCESSES)

# Initialize Redis
try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        socket_timeout=5,
        socket_connect_timeout=5,
        decode_responses=False
    )
    redis_client.ping()
    logger.info("Redis connected successfully")
except redis.ConnectionError as e:
    logger.error(f"Redis connection error: {e}")
    redis_client = None

# Initialize APIs
spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
) if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET else None

# Initialize Bot
app = Client(
    "JhoomMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Initialize PyTgCalls
pytgcalls = PyTgCalls(app)
pytgcalls._init_js = False  # Disable unnecessary JavaScript initialization

# Database Setup
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo.jhoommusic
start_time = time.time()

# Collections
users = db.users
chats = db.chats
blocked_users = db.blocked_users
blacklisted_chats = db.blacklisted_chats
auth_users = db.auth_users
channel_connections = db.channel_connections
channel_queues = db.channel_queues
gbanned_users = db.gbanned_users
playlists = db.playlists
user_settings = db.user_settings
thumbnails = db.thumbnails
troubleshooting_logs = db.troubleshooting_logs

# Create database indexes
async def create_indexes():
    try:
        await users.create_index("user_id", unique=True)
        await chats.create_index("chat_id", unique=True)
        await blocked_users.create_index("user_id", unique=True)
        await auth_users.create_index("user_id", unique=True)
        await gbanned_users.create_index("user_id", unique=True)
        await playlists.create_index([("user_id", 1), ("name", 1)], unique=True)
        await channel_queues.create_index([("chat_id", 1), ("timestamp", -1)])
        await user_settings.create_index([("chat_id", 1), ("user_id", 1)])
        await thumbnails.create_index("key", unique=True)
        await troubleshooting_logs.create_index([("chat_id", 1), ("timestamp", -1)])
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.error(f"Error creating database indexes: {e}")

asyncio.get_event_loop().run_until_complete(create_indexes())

# Global Variables
current_streams: Dict[int, Dict] = {}
loop_status: Dict[int, Dict[str, Union[str, int]]] = {}
shuffle_status: Dict[int, bool] = {}
message_history: Dict[int, List[int]] = {}
user_last_command = defaultdict(dict)
active_repairs = set()

# ======================
# COMMAND DETAILS
# ======================

COMMAND_DETAILS = {
    "sultan": {
        "title": "SULTAN COMMAND",
        "description": "MUSIC PLAYBACK CONTROLS",
        "commands": [
            "/pause :- PAUSE CURRENT PLAYING STREAM",
            "/resume :- RESUME PAUSED STREAM",
            "/skip :- SKIP TO NEXT TRACK IN QUEUE",
            "/stop :- CLEAN QUEUE AND END STREAM",
            "/player :- GET INTERACTIVE PLAYER PANEL",
            "/end :- END THE STREAM",
            "/queue :- SHOW QUEUED TRACKS LIST"
        ]
    },
    "license": {
        "title": "LICENSE COMMAND",
        "description": "USER AUTHORIZATION SYSTEM",
        "commands": [
            "/auth user_id :- ADD USER TO AUTH LIST",
            "/unauth user_id :- REMOVE USER FROM AUTH LIST",
            "/authusers :- SHOWS LIST OF AUTH USERS"
        ]
    },
    "broadcast": {
        "title": "BROADCAST COMMAND",
        "description": "MESSAGE BROADCASTING SYSTEM",
        "commands": [
            "/broadcast text :- BROADCAST TO ALL CHATS",
            "/broadcast -pin :- PIN BROADCASTED MESSAGES",
            "/broadcast -pinloud :- PIN WITH NOTIFICATION",
            "/broadcast -user :- BROADCAST TO USERS",
            "/broadcast -assistant :- BROADCAST FROM ASSISTANT",
            "/broadcast -nobot :- FORCE BOT TO NOT BROADCAST"
        ]
    },
    "block": {
        "title": "BLOCK COMMAND",
        "description": "USER BLOCKING SYSTEM",
        "commands": [
            "/block username :- BLOCK USER FROM BOT",
            "/unblock username :- UNBLOCK USER",
            "/blockedusers :- SHOWS BLOCKED USERS LIST"
        ]
    },
    "blacklist": {
        "title": "BLACKLIST COMMAND",
        "description": "CHAT BLACKLIST SYSTEM",
        "commands": [
            "/blacklistchat chat_id :- BLACKLIST CHAT",
            "/whitelistchat chat_id :- WHITELIST CHAT",
            "/blacklistedchat :- SHOWS BLACKLISTED CHATS"
        ]
    },
    "channel": {
        "title": "CHANNEL-PLAY COMMAND",
        "description": "CHANNEL STREAMING CONTROLS",
        "commands": [
            "/cplay :- STREAM AUDIO IN CHANNEL",
            "/cvplay :- STREAM VIDEO IN CHANNEL",
            "/cplayforce :- FORCE PLAY NEW TRACK",
            "/channelplay :- CONNECT CHANNEL TO GROUP"
        ]
    },
    "speed": {
        "title": "SPEEDTEST COMMAND",
        "description": "PLAYBACK SPEED CONTROLS",
        "commands": [
            "/speed :- ADJUST PLAYBACK SPEED IN GROUP",
            "/cSpeed :- ADJUST SPEED IN CHANNEL"
        ]
    },
    "song": {
        "title": "SONG COMMAND",
        "description": "TRACK DOWNLOAD SYSTEM",
        "commands": [
            "/song url/name :- DOWNLOAD TRACK FROM YOUTUBE"
        ]
    },
    "seek": {
        "title": "SEEK COMMAND",
        "description": "PLAYBACK POSITION CONTROL",
        "commands": [
            "/seek time-dur :- SEEK TO POSITION",
            "/seekback time-dur :- SEEK BACKWARDS"
        ]
    },
    "shuffle": {
        "title": "SHUFFLE COMMANDS",
        "description": "QUEUE MANAGEMENT",
        "commands": [
            "/shuffle :- SHUFFLE THE QUEUE",
            "/queue :- SHOW SHUFFLED QUEUE"
        ]
    },
    "vplay": {
        "title": "VPLAY COMMAND",
        "description": "VIDEO STREAMING CONTROLS",
        "commands": [
            "/vplay :- START VIDEO STREAM",
            "/vplayforce :- FORCE NEW VIDEO STREAM"
        ]
    },
    "ping": {
        "title": "PING COMMAND",
        "description": "BOT STATUS SYSTEM",
        "commands": [
            "/ping :- SHOW BOT PING AND STATS",
            "/stats :- SHOW BOT STATISTICS",
            "/uptime :- SHOW BOT UPTIME"
        ]
    },
    "revamp": {
        "title": "REVAMP COMMAND",
        "description": "BOT MAINTENANCE CONTROLS",
        "commands": [
            "/logs :- GET BOT LOGS",
            "/logger :- TOGGLE ACTIVITY LOGGING",
            "/maintenance :- TOGGLE MAINTENANCE MODE"
        ]
    },
    "spiral": {
        "title": "SPIRAL COMMAND",
        "description": "LOOPING CONTROLS",
        "commands": [
            "/loop enable/disable :- TOGGLE LOOP",
            "/loop 1/2/3 :- SET LOOP COUNT"
        ]
    },
    "gbans": {
        "title": "G-BANS COMMAND",
        "description": "GLOBAL BAN SYSTEM",
        "commands": [
            "/gban user_id :- GLOBALLY BAN USER",
            "/ungban user_id :- REMOVE GLOBAL BAN",
            "/gbannedusers :- SHOW GLOBALLY BANNED USERS"
        ]
    },
    "troubleshoot": {
        "title": "TROUBLESHOOT COMMANDS",
        "description": "SELF-REPAIR SYSTEM",
        "commands": [
            "/fixbot :- REPAIR COMMON ISSUES",
            "/diagnose :- CHECK BOT HEALTH",
            "/fixproblem :- (ADMIN ONLY) REMOTE REPAIRS"
        ]
    },
    "settings": {
        "title": "SETTINGS COMMAND",
        "description": "USER PREFERENCES SYSTEM",
        "commands": [
            "/settings :- SHOW SETTINGS PANEL",
            "/settings volume [1-200] :- SET PLAYBACK VOLUME",
            "/settings quality [low|medium|high] :- SET STREAM QUALITY",
            "/settings language [en|hi|etc] :- SET BOT LANGUAGE",
            "/settings notifications [on|off] :- TOGGLE NOTIFICATIONS"
        ]
    },
    "radio": {
        "title": "RADIO COMMAND",
        "description": "GLOBAL FM RADIO SYSTEM",
        "commands": [
            "/radio search [query] :- SEARCH RADIO STATIONS",
            "/radio play [ID] :- PLAY RADIO STATION",
            "/radio stop :- STOP RADIO PLAYBACK",
            "/radio list :- SHOW POPULAR STATIONS"
        ]
    }
}

# ======================
# RADIO PLAYBACK SYSTEM (VC + BROWSER + GARDEN)
# ======================

@app.on_message(filters.command(["radio", "fm"]) & filters.group)
async def radio_command_handler(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    args = message.text.split(None, 2)

    if len(args) < 2:
        return await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="**Usage:** `/radio search [query]` or `/radio play [ID]`"
        )

    subcmd = args[1].lower()

    if subcmd == "search" and len(args) >= 3:
        query = args[2]
        stations = []

        try:
            async with aiohttp.ClientSession() as session:
                # Radio Browser search
                async with session.get(f"https://de1.api.radio-browser.info/json/stations/search?name={query}") as response:
                    if response.status == 200:
                        stations = await response.json()

                if not stations:
                    # Radio Garden fallback search
                    async with session.get(f"http://radio.garden/api/ara/content/search?query={query}") as response:
                        if response.status == 200:
                            garden_data = await response.json()
                            if garden_data.get("hits"):
                                for i, hit in enumerate(garden_data["hits"][:5], 1):
                                    stations.append({
                                        "name": hit["title"],
                                        "id": hit["id"],
                                        "source": "garden"
                                    })
        except Exception as e:
            logger.error(f"Radio Search error: {e}")
            return await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption="❌ Error while searching radio stations"
            )

        if not stations:
            return await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption="❌ No station found."
            )

        reply_text = "📻 **Top 5 Radio Stations**\n\n"
        for i, station in enumerate(stations[:5], 1):
            reply_text += f"`{i}`. {station['name']}\n"
        reply_text += "\n🎧 Use `/radio play [ID]` to listen."
        return await message.reply_photo(
            photo=UI_IMAGES["radio"],
            caption=reply_text
        )

    elif subcmd == "play" and len(args) >= 3:
        try:
            station_index = int(args[2]) - 1
            stream_url = None
            station_title = "Live Radio"

            async with aiohttp.ClientSession() as session:
                # Radio Browser play
                async with session.get("https://de1.api.radio-browser.info/json/stations/search?name=all") as response:
                    if response.status == 200:
                        stations = await response.json()

                if station_index < len(stations):
                    station = stations[station_index]
                    stream_url = station.get("url_resolved")
                    station_title = station.get("name")
                else:
                    # Radio Garden fallback play
                    fallback_index = station_index - len(stations)
                    async with session.get("http://radio.garden/api/ara/content/search?query=all") as response:
                        if response.status == 200:
                            garden_data = await response.json()
                            if garden_data.get("hits") and fallback_index < len(garden_data["hits"]):
                                station_id = garden_data["hits"][fallback_index]["id"]
                                station_title = garden_data["hits"][fallback_index].get("title", "Live Radio")
                                stream_url = f"http://radio.garden/api/ara/content/listen/{station_id}/channel.mp3"

            if not stream_url:
                return await message.reply_photo(
                    photo=UI_IMAGES["error"],
                    caption="❌ Stream URL not found"
                )

            track_info = {
                'title': station_title,
                'artist': 'Live Radio',
                'duration': 0,
                'url': stream_url,
                'source': 'radio',
                'is_live': True,
                'user_id': user_id,
                'thumbnail': "https://i.imgur.com/JnPE5aN.png"
            }

            if chat_id in current_streams:
                await queue_manager.add_to_queue(chat_id, track_info)
                return await message.reply_photo(
                    photo=UI_IMAGES["success"],
                    caption=f"📻 Added to queue: {station_title}"
                )
            else:
                current_streams[chat_id] = track_info
                await play_next_track(chat_id)
                return await message.reply_photo(
                    photo=UI_IMAGES["success"],
                    caption=f"📻 Now Playing: {station_title}"
                )

        except Exception as e:
            logger.error(f"Radio Play error: {e}")
            return await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption="❌ Failed to play radio station"
            )

    elif subcmd == "stop":
        if chat_id in current_streams and current_streams[chat_id].get('source') == 'radio':
            await connection_manager.release_connection(chat_id)
            del current_streams[chat_id]
            await message.reply_photo(
                photo=UI_IMAGES["success"],
                caption="⏹ Stopped radio playback"
            )
        else:
            await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption="❌ No radio playback to stop"
            )

    elif subcmd == "list":
        popular_stations = [
            ("BBC Radio 1", "1"),
            ("Radio FM4", "2"),
            ("KEXP Seattle", "3"),
            ("Radio Paradise", "4"),
            ("SomaFM Groove Salad", "5")
        ]

        text = "📻 Popular Radio Stations:\n\n"
        for name, id in popular_stations:
            text += f"- {name} (use /radio play {id})\n"

        await message.reply_photo(
            photo=UI_IMAGES["radio"],
            caption=text
        )

    else:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="**Usage:** `/radio search [query]` or `/radio play [ID]`"
        )

# ======================
# SYSTEM STATUS FUNCTIONS
# ======================

async def get_system_status() -> str:
    """Generate comprehensive system status report"""
    # Get system metrics
    ram = psutil.virtual_memory().used // (1024 * 1024)  # MB
    cpu = psutil.cpu_percent()
    uptime = get_uptime()
    
    # Get FFMPEG thread count
    ffmpeg_threads = len([p for p in psutil.process_iter() if 'ffmpeg' in p.name().lower()])
    
    # Database statuses
    try:
        redis_status = "CONNECTED" if redis_client and redis_client.ping() else "DISCONNECTED"
    except:
        redis_status = "DISCONNECTED"
    
    try:
        await mongo.admin.command('ping')
        mongo_status = "OK"
    except:
        mongo_status = "ERROR"
    
    # Get counts from database
    total_chats = await chats.count_documents({})
    total_users = await users.count_documents({})
    
    # Get cache keys count if Redis is connected
    cache_keys = 0
    if redis_status == "CONNECTED":
        try:
            cache_keys = await asyncio.get_event_loop().run_in_executor(
                executor,
                lambda: redis_client.dbsize()
            )
        except:
            pass
    
    # Other system info
    ping_time = round((await app.get_me()).last_online_date.timestamp() - time.time(), 2)
    os_name = f"{platform.system()} {platform.release()}"
    python_version = platform.python_version()
    pyrogram_version = pyrogram.__version__
    bot_version = "1.0"
    last_restart = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate health score (simple example)
    score = 100
    if cpu > 80: score -= 10
    if redis_status != "CONNECTED": score -= 20
    if mongo_status != "OK": score -= 20
    score = max(0, score)
    
    # Redis status with colored text
    if redis_status == "CONNECTED":
        redis_status_text = f"🟢 {redis_status}"
    else:
        redis_status_text = f"🔴 {redis_status} - Please check connection!"
    
    # MongoDB status with colored text
    if mongo_status == "OK":
        mongo_status_text = f"🟢 {mongo_status}"
    else:
        mongo_status_text = f"🔴 {mongo_status} - Please check server!"
    
    # Format the system status message
    text = f"""╭────────── JHOOM CORE SYSTEM UNIT ──────────╮

  SYSTEM STATUS
  • RAM        :: {ram} MB
  • CPU        :: {cpu}% {'🔴 High CPU usage!' if cpu > 80 else ''}
  • UPTIME     :: {uptime}
  • FFMPEG     :: {ffmpeg_threads} active threads

  DATABASE STATUS
  • REDIS      :: {redis_status_text}
  • MONGODB    :: {mongo_status_text}
  • GROUPS     :: {total_chats}
  • USERS      :: {total_users}
  • CACHE KEYS :: {cache_keys}

  NETWORK & SYSTEM
  • PING       :: {ping_time}ms
  • HOST       :: {os_name}
  • PYTHON     :: {python_version}
  • LIBRARY    :: Pyrogram {pyrogram_version}
  • VERSION    :: {bot_version}
  • RESTARTED  :: {last_restart}

  CORE STATUS :: {'SYSTEM STABLE' if score > 80 else 'SYSTEM WARNING'} | HEALTH SCORE :: {score}%

╰────────────────────────────────────────────╯

Powered by **Jhoom Music**

Copyright © 2025 **Jhoom Music**. All rights reserved.
"""
    return text

# ======================
# CORE COMPONENTS
# ======================

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        self.lock = asyncio.Lock()
    
    async def get_connection(self, chat_id: int) -> bool:
        async with self.lock:
            if chat_id in self.active_connections:
                return True
            
            try:
                await pytgcalls.join_group_call(
                    chat_id,
                    AudioPiped("http://example.com", HighQualityAudio())
                )
                self.active_connections[chat_id] = True
                return True
            except Exception as e:
                logger.error(f"Connection error for {chat_id}: {e}")
                return False
    
    async def release_connection(self, chat_id: int) -> None:
        async with self.lock:
            if chat_id in self.active_connections:
                try:
                    await pytgcalls.leave_group_call(chat_id)
                except Exception as e:
                    logger.error(f"Error leaving call {chat_id}: {e}")
                del self.active_connections[chat_id]

connection_manager = ConnectionManager()

class QueueManager:
    def __init__(self):
        self.queues = defaultdict(list)
        self.locks = defaultdict(asyncio.Lock)
    
    async def add_to_queue(self, chat_id: int, track: Dict) -> None:
        async with self.locks[chat_id]:
            if len(self.queues[chat_id]) >= MAX_QUEUE_SIZE:
                raise Exception(f"Queue limit reached ({MAX_QUEUE_SIZE} tracks)")
                
            self.queues[chat_id].append(track)
            await channel_queues.insert_one({
                "chat_id": chat_id,
                "track": track,
                "timestamp": datetime.utcnow()
            })
    
    async def get_next_track(self, chat_id: int) -> Optional[Dict]:
        async with self.locks[chat_id]:
            if chat_id in self.queues and self.queues[chat_id]:
                track = self.queues[chat_id].pop(0)
                await channel_queues.delete_one({
                    "chat_id": chat_id,
                    "track.title": track['title']
                })
                return track
            
            db_track = await channel_queues.find_one(
                {"chat_id": chat_id},
                sort=[("timestamp", 1)]
            )
            
            if db_track:
                await channel_queues.delete_one({"_id": db_track["_id"]})
                return db_track['track']
            return None
    
    async def clear_queue(self, chat_id: int) -> None:
        async with self.locks[chat_id]:
            if chat_id in self.queues:
                self.queues[chat_id].clear()
            await channel_queues.delete_many({"chat_id": chat_id})

queue_manager = QueueManager()

class ProcessManager:
    def __init__(self):
        self.max_processes = FFMPEG_PROCESSES
        self.current_processes = 0
        self.lock = asyncio.Lock()
    
    async def adjust_processes(self) -> None:
        async with self.lock:
            try:
                load = os.getloadavg()[0]
            except:
                load = 0
            
            if load > 2.0 and self.max_processes > 2:
                new_max = max(2, self.max_processes - 2)
                logger.info(f"Reducing FFmpeg processes from {self.max_processes} to {new_max}")
                self.max_processes = new_max
            elif load < 1.0 and self.max_processes < FFMPEG_PROCESSES:
                new_max = min(FFMPEG_PROCESSES, self.max_processes + 2)
                logger.info(f"Increasing FFmpeg processes from {self.max_processes} to {new_max}")
                self.max_processes = new_max
            
            if executor._max_workers != self.max_processes:
                executor._max_workers = self.max_processes
    
    async def get_executor(self) -> concurrent.futures.ThreadPoolExecutor:
        await self.adjust_processes()
        return executor

process_manager = ProcessManager()

# ======================
# HELPER FUNCTIONS
# ======================

def get_uptime() -> str:
    seconds = int(time.time() - start_time)
    periods = [('day', 86400), ('hour', 3600), ('minute', 60), ('second', 1)]
    return ", ".join(
        f"{val} {name}{'s' if val > 1 else ''}"
        for name, sec in periods
        if (val := seconds // sec) > 0
    )

def get_current_time() -> str:
    return datetime.now().strftime('%H:%M')

def format_duration(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"

async def is_admin_or_sudo(chat_id: int, user_id: int) -> bool:
    if user_id in SUDO_USERS:
        return True
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except Exception:
        return False

async def is_user_gbanned(user_id: int) -> bool:
    return await gbanned_users.find_one({"user_id": user_id}) is not None

async def check_user_auth(user_id: int) -> bool:
    if user_id in SUDO_USERS:
        return True
    return await auth_users.find_one({"user_id": user_id}) is not None

async def cleanup_messages(chat_id: int, keep_last: int = None):
    settings = await user_settings.find_one({"chat_id": chat_id}) or {}
    keep_last = settings.get("keep_messages", keep_last or 5)
    
    if chat_id in message_history and len(message_history[chat_id]) > keep_last:
        for msg_id in message_history[chat_id][:-keep_last]:
            try:
                await app.delete_messages(chat_id, msg_id)
            except Exception as e:
                logger.error(f"Error deleting message {msg_id}: {e}")
        message_history[chat_id] = message_history[chat_id][-keep_last:]

def get_ffmpeg_options(chat_id: int, is_video: bool = False) -> Dict:
    base_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn' if not is_video else ''
    }
    
    if chat_id < 0:  # Group chat
        base_options['options'] += ' -bufsize 1024k'
    else:  # Private chat
        base_options['options'] += ' -bufsize 512k'
    
    base_options['options'] += f' -threads {min(FFMPEG_PROCESSES, 8)}'
    return base_options

def extract_chat_id(message: Message) -> int:
    """Extract chat ID from message text or reply"""
    if message.reply_to_message:
        return message.reply_to_message.chat.id
    try:
        return int(message.text.split()[1])
    except (IndexError, ValueError):
        return message.chat.id

# ======================
# TROUBLESHOOTING SYSTEM
# ======================

async def log_troubleshooting_action(chat_id: int, action: str, status: str, details: str = ""):
    await troubleshooting_logs.insert_one({
        "chat_id": chat_id,
        "action": action,
        "status": status,
        "details": details,
        "timestamp": datetime.utcnow(),
        "bot_uptime": get_uptime()
    })

async def fix_voice_connection(chat_id: int):
    if chat_id in active_repairs:
        return
    active_repairs.add(chat_id)
    
    try:
        await log_troubleshooting_action(chat_id, "voice_fix", "started")
        await pytgcalls.leave_group_call(chat_id)
        await asyncio.sleep(2)
        
        if not await connection_manager.get_connection(chat_id):
            raise Exception("Failed to establish new connection")
        
        if chat_id in current_streams:
            await play_next_track(chat_id, same_track=True)
        
        await log_troubleshooting_action(chat_id, "voice_fix", "success")
        await app.send_message(
            chat_id,
            "✅ Voice connection successfully repaired"
        )
    except Exception as e:
        logger.error(f"Voice fix error in {chat_id}: {e}")
        await log_troubleshooting_action(chat_id, "voice_fix", "failed", str(e))
        await notify_failure(chat_id, str(e))
    finally:
        active_repairs.discard(chat_id)

async def restart_playback(chat_id: int):
    if chat_id in active_repairs:
        return
    active_repairs.add(chat_id)
    
    try:
        await log_troubleshooting_action(chat_id, "playback_restart", "started")
        if chat_id in current_streams:
            await play_next_track(chat_id, same_track=True)
            await log_troubleshooting_action(chat_id, "playback_restart", "success")
            await app.send_message(
                chat_id,
                "✅ Playback successfully restarted"
            )
        else:
            await log_troubleshooting_action(chat_id, "playback_restart", "failed", "No current stream")
            await app.send_message(
                chat_id,
                "❌ No active playback to restart"
            )
    except Exception as e:
        logger.error(f"Playback restart error in {chat_id}: {e}")
        await log_troubleshooting_action(chat_id, "playback_restart", "failed", str(e))
        await notify_failure(chat_id, str(e))
    finally:
        active_repairs.discard(chat_id)

async def restart_bot_in_chat(chat_id: int):
    if chat_id in active_repairs:
        return
    active_repairs.add(chat_id)
    
    try:
        await log_troubleshooting_action(chat_id, "bot_restart", "started")
        chat = await app.get_chat(chat_id)
        await app.leave_chat(chat_id)
        await asyncio.sleep(3)
        
        if chat.invite_link:
            await app.join_chat(chat.invite_link)
            await log_troubleshooting_action(chat_id, "bot_restart", "success")
            await app.send_message(
                chat_id,
                "✅ Bot successfully rejoined the group"
            )
        else:
            error_msg = "No invite link available"
            await log_troubleshooting_action(chat_id, "bot_restart", "failed", error_msg)
            await app.send_message(
                SUPER_GROUP_ID,
                f"❌ Bot restart failed in {chat.title}\n"
                f"Reason: {error_msg}"
            )
    except Exception as e:
        logger.error(f"Bot restart error in {chat_id}: {e}")
        await log_troubleshooting_action(chat_id, "bot_restart", "failed", str(e))
        await notify_failure(chat_id, str(e))
    finally:
        active_repairs.discard(chat_id)

async def check_and_request_permissions(chat_id: int):
    required_perms = {
        "can_manage_voice_chats": "Manage Voice Chats",
        "can_delete_messages": "Delete Messages",
        "can_invite_users": "Invite Users"
    }
    
    try:
        me = await app.get_chat_member(chat_id, "me")
        missing_perms = [
            name for perm, name in required_perms.items() 
            if not getattr(me, perm, False)
        ]
        
        if missing_perms:
            await app.send_message(
                chat_id,
                "⚠️ Missing Permissions:\n\n" +
                "\n".join(f"• {name}" for name in missing_perms) +
                f"\n\nPlease grant these permissions to @{(await app.get_me()).username}"
            )
            await log_troubleshooting_action(
                chat_id, 
                "permission_check", 
                "missing_perms", 
                ", ".join(missing_perms)
            )
        else:
            await app.send_message(
                chat_id,
                "✅ All required permissions are available"
            )
            await log_troubleshooting_action(
                chat_id, 
                "permission_check", 
                "success"
            )
    except Exception as e:
        logger.error(f"Permission check error in {chat_id}: {e}")
        await log_troubleshooting_action(
            chat_id, 
            "permission_check", 
            "failed", 
            str(e)
        )
        await notify_failure(chat_id, str(e))

async def notify_failure(chat_id: int, error: str):
    error_msg = (
        f"❌ Automatic repair failed\n\n"
        f"Error: {error[:200]}\n\n"
        f"Please contact @{SUPER_GROUP_USERNAME} for assistance"
    )
    
    try:
        await app.send_message(chat_id, error_msg)
    except Exception as e:
        logger.error(f"Failed to send failure notification to {chat_id}: {e}")
    
    await app.send_message(
        SUPER_GROUP_ID,
        f"🚨 Repair Failed\n"
        f"Chat ID: {chat_id}\n"
        f"Error: {error}\n\n"
        f"Manual intervention required"
    )

async def run_diagnostics(chat_id: int) -> str:
    report = ["🔍 Diagnostic Report"]
    
    # Connection status
    conn_status = "✅" if chat_id in current_streams else "❌"
    report.append(f"{conn_status} Voice Connection")
    
    # Permission check
    try:
        me = await app.get_chat_member(chat_id, "me")
        perms = [
            ("Manage Voice Chats", me.can_manage_voice_chats),
            ("Delete Messages", me.can_delete_messages),
            ("Invite Users", me.can_invite_users)
        ]
        for name, status in perms:
            report.append(f"{'✅' if status else '❌'} {name}")
    except Exception as e:
        report.append(f"❓ Permission Check Failed: {str(e)[:50]}")
    
    # Queue status
    queue_len = len(queue_manager.queues.get(chat_id, []))
    report.append(f"📊 Queue Length: {queue_len}")
    
    # Bot status
    report.append(f"🔄 Bot Uptime: {get_uptime()}")
    
    # Suggested actions
    if "❌" in "\n".join(report):
        report.append("\n🚀 Suggested Action: Use /fixbot command")
    
    return "\n".join(report)

async def check_all_groups_health():
    try:
        all_chats = await chats.find().to_list(None)
        for chat in all_chats:
            chat_id = chat["chat_id"]
            try:
                # Skip if already being repaired
                if chat_id in active_repairs:
                    continue
                    
                # Check voice connection
                if chat_id in current_streams:
                    participants = await pytgcalls.get_participants(chat_id)
                    if len(participants) <= 1:  # Only bot in call
                        await log_troubleshooting_action(
                            chat_id,
                            "health_check",
                            "no_listeners",
                            "Only bot in voice chat"
                        )
                        await pytgcalls.leave_group_call(chat_id)
            except Exception as e:
                logger.error(f"Health check error for {chat_id}: {e}")
                await log_troubleshooting_action(
                    chat_id,
                    "health_check",
                    "failed",
                    str(e)
                )
    except Exception as e:
        logger.error(f"Global health check error: {e}")

# ======================
# TROUBLESHOOTING COMMANDS
# ======================

@app.on_message(filters.command("fixproblem") & filters.chat(SUPER_GROUP_ID))
async def problem_fix_menu(_, message: Message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔊 Voice Connection", callback_data="fix_voice")],
        [InlineKeyboardButton("🛑 Playback Stopped", callback_data="fix_playback")],
        [InlineKeyboardButton("📛 Permissions Issue", callback_data="fix_permission")],
        [InlineKeyboardButton("🔍 Other Problem", callback_data="fix_other")]
    ])
    
    await message.reply_photo(
        photo=UI_IMAGES["admin"],
        caption="⚠️ Select problem type to fix:",
        reply_markup=buttons
    )

@app.on_message(filters.command(["fixbot", "repair"]))
async def user_fix_command(_, message: Message):
    chat = message.chat
    user = message.from_user
    
    if not await is_admin_or_sudo(chat.id, user.id):
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ Only admins can use this command"
        )
        return
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Restart Bot", callback_data=f"userfix_restart_{chat.id}")],
        [InlineKeyboardButton("🎧 Rejoin Voice", callback_data=f"userfix_join_{chat.id}")],
        [InlineKeyboardButton("📜 Check Perms", callback_data=f"userfix_perms_{chat.id}")],
        [InlineKeyboardButton("🚨 Report to Support", url=f"t.me/{SUPER_GROUP_USERNAME}")]
    ])
    
    await message.reply_photo(
        photo=UI_IMAGES["diagnostics"],
        caption=f"🔧 {user.mention}, select repair option:\n\n"
        f"Group: {chat.title}\n"
        f"Problem ID: {hash(str(chat.id)[-4:])}",
        reply_markup=buttons
    )

@app.on_message(filters.command("diagnose"))
async def diagnose_command(_, message: Message):
    chat_id = message.chat.id
    if not await is_admin_or_sudo(chat_id, message.from_user.id):
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ Only admins can use this command"
        )
        return
    
    try:
        report = await run_diagnostics(chat_id)
        await message.reply_photo(
            photo=UI_IMAGES["diagnostics"],
            caption=report
        )
    except Exception as e:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption=f"❌ Diagnostic failed: {str(e)[:200]}"
        )

@app.on_callback_query(filters.regex("^fix_"))
async def supergroup_fix_handler(_, query: CallbackQuery):
    problem_type = query.data.split("_")[1]
    chat_id = extract_chat_id(query.message)
    
    if problem_type == "voice":
        await fix_voice_connection(chat_id)
    elif problem_type == "playback":
        await restart_playback(chat_id)
    elif problem_type == "permission":
        await check_and_request_permissions(chat_id)
    elif problem_type == "other":
        await query.answer("Please describe the issue in group chat", show_alert=True)
        return
    
    await query.answer(f"Repair initiated for {problem_type}")

@app.on_callback_query(filters.regex("^userfix_"))
async def user_fix_handler(_, query: CallbackQuery):
    action, chat_id = query.data.split("_")[1:]
    chat_id = int(chat_id)
    
    if action == "restart":
        await restart_bot_in_chat(chat_id)
    elif action == "join":
        await fix_voice_connection(chat_id)
    elif action == "perms":
        await check_and_request_permissions(chat_id)
    
    await query.answer(f"Repair action: {action}")

# ======================
# MUSIC PLAYBACK SYSTEM
# ======================

@pytgcalls.on_stream_end()
async def on_stream_end(client: PyTgCalls, update: Update):
    chat_id = update.chat_id
    await cleanup_messages(chat_id)

    if chat_id in loop_status:
        if loop_status[chat_id]['type'] == 'track' and loop_status[chat_id]['count'] > 0:
            loop_status[chat_id]['count'] -= 1
            if loop_status[chat_id]['count'] > 0:
                await play_next_track(chat_id, same_track=True)
                return
        
        elif loop_status[chat_id]['type'] == 'queue' and chat_id in current_streams:
            loop_status[chat_id]['count'] -= 1
            if loop_status[chat_id]['count'] > 0:
                await queue_manager.add_to_queue(chat_id, current_streams[chat_id])
                await play_next_track(chat_id)
                return

    await play_next_track(chat_id)

async def play_next_track(chat_id: int, same_track: bool = False):
    try:
        if same_track and chat_id in current_streams:
            track = current_streams[chat_id]
        else:
            track = await queue_manager.get_next_track(chat_id)
            if not track:
                if chat_id in current_streams:
                    del current_streams[chat_id]
                
                if chat_id not in loop_status or loop_status[chat_id]['count'] == 0:
                    await connection_manager.release_connection(chat_id)
                    await app.send_photo(
                        chat_id, 
                        UI_IMAGES["player"], 
                        caption="⏹ Playback ended"
                    )
                
                if chat_id in loop_status:
                    del loop_status[chat_id]
                return
            
            current_streams[chat_id] = track
        
        thumb = await generate_advanced_music_thumbnail(
            title=track['title'],
            channel=track.get('artist', 'Unknown Artist'),
            views=track.get('views', '0 views'),
            duration=str(timedelta(seconds=track.get('duration', 0))),
            current_time="00:00",
            query_by="User",
            cover_url=track.get('thumbnail'),
            bot_user_id=app.me.id,
            requester_id=track.get('user_id'),
            progress_percentage=0.0
        )
        
        ffmpeg_opts = get_ffmpeg_options(chat_id, track.get('is_video', False))
        
        if not await connection_manager.get_connection(chat_id):
            await app.send_message(chat_id, "❌ Failed to establish connection")
            return
        
        if track.get('is_video', False):
            stream = AudioVideoPiped(
                track['url'],
                audio_parameters=HighQualityAudio(),
                video_parameters=HighQualityVideo(),
                **ffmpeg_opts
            )
        else:
            stream = AudioPiped(
                track['url'],
                audio_parameters=HighQualityAudio(),
                **ffmpeg_opts
            )
        
        await pytgcalls.change_stream(chat_id, stream)
        
        caption = f"🎵 **Now Playing**\n\n" \
                 f"**Title**: {track['title']}\n" \
                 f"**Artist**: {track.get('artist', 'Unknown')}\n" \
                 f"**Duration**: {format_duration(track.get('duration', 0))}\n" \
                 f"**Source**: {track.get('source', 'Unknown').capitalize()}"
        
        msg = await app.send_photo(
            chat_id,
            photo=thumb,
            caption=caption
        )
        
        if chat_id not in message_history:
            message_history[chat_id] = []
        message_history[chat_id].append(msg.id)
        
    except NoActiveGroupCall:
        await connection_manager.release_connection(chat_id)
        if chat_id in current_streams:
            del current_streams[chat_id]
        await app.send_message(
            chat_id,
            "❌ No active voice chat. Please start a voice chat first."
        )
    except Exception as e:
        logger.error(f"Playback error in chat {chat_id}: {e}")
        await app.send_message(chat_id, f"❌ Playback error: {str(e)}")

# ======================
# THUMBNAIL GENERATION
# ======================

async def generate_advanced_music_thumbnail(
    title: str,
    channel: str,
    views: str,
    duration: str,
    current_time: str,
    query_by: str,
    cover_url: Optional[str] = None,
    bot_user_id: int = None,
    requester_id: int = None,
    progress_percentage: float = 0.0
) -> BytesIO:
    try:
        cache_key = f"thumb_{hashlib.md5(title.encode()).hexdigest()}"
        cached_thumb = await get_cached_data(cache_key)
        if cached_thumb:
            return BytesIO(cached_thumb)
        
        img = Image.new("RGB", (800, 600), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Gradient background
        for y in range(600):
            r = int(20 + (y * 0.1))
            g = int(20 + (y * 0.05))
            b = int(30 + (y * 0.07))
            draw.line([(0, y), (800, y)], fill=(r, g, b))
        
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 36)
            font_header = ImageFont.truetype("arialbd.ttf", 28)
            font_info = ImageFont.truetype("arial.ttf", 24)
            font_time = ImageFont.truetype("arialbd.ttf", 32)
            font_event = ImageFont.truetype("arial.ttf", 22)
        except:
            font_title = font_header = font_info = font_time = font_event = ImageFont.load_default()

        # Album cover with shadow effect
        if cover_url:
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    lambda: requests.get(cover_url, timeout=5)
                )
                cover_img = Image.open(BytesIO(response.content)).convert("RGB")
                cover_img = cover_img.resize((350, 350), Image.LANCZOS)
                
                # Create shadow effect
                shadow = Image.new('RGBA', (360, 360), (0, 0, 0, 100))
                for x in range(360):
                    for y in range(360):
                        if x < 350 and y < 350:
                            shadow.putpixel((x, y), (0, 0, 0, 0))
                
                img.paste(shadow, (175, 125), shadow)
                border_img = Image.new('RGB', (354, 354), (255, 255, 255))
                border_img.paste(cover_img, (2, 2))
                img.paste(border_img, (178, 128))
            except Exception as e:
                logger.error(f"Cover image error: {e}")

        # Text with shadow effect
        def draw_text_with_shadow(x, y, text, font, fill, shadowcolor=(0, 0, 0)):
            draw.text((x+2, y+2), text, font=font, fill=shadowcolor)
            draw.text((x, y), text, font=font, fill=fill)

        # Header text
        draw_text_with_shadow(50, 50, "# MUSIC", font_header, (255, 255, 255))
        draw_text_with_shadow(50, 90, f"Channel - {channel} Views - {views}", 
                            font_info, (200, 200, 200))

        # Time indicators
        draw_text_with_shadow(650, 100, current_time, font_time, (255, 255, 255))
        draw_text_with_shadow(650, 150, duration, font_time, (255, 255, 255))

        # Progress bar background
        for x in range(50, 750):
            alpha = x / 700
            r = int(100 + (100 * alpha))
            g = int(100 + (50 * alpha))
            b = 100
            draw.line([(x, 180), (x+1, 180)], fill=(r, g, b), width=2)

        # Rainbow title effect
        for i, c in enumerate(title):
            hue = i / len(title)
            r = int(255 * (1 - hue/2))
            g = int(255 * (0.5 + hue/3))
            b = int(255 * hue)
            draw.text((50 + i*18, 200), c, font=font_title, fill=(r, g, b))

        # Progress bar
        progress_width = int(700 * progress_percentage)
        for i in range(3):
            draw.rounded_rectangle([50-i, 380-i, 50+progress_width+i, 390+i], 
                                 radius=5, fill=(0, 100+i*50, 0))
        draw.rounded_rectangle([50, 380, 50+progress_width, 390], 
                             radius=5, fill=(0, 255, 0))

        # Bot profile image
        if bot_user_id:
            try:
                bot_photos = await app.get_profile_photos(bot_user_id, limit=1)
                if bot_photos:
                    bot_photo = await app.download_media(bot_photos[0].file_id, in_memory=True)
                    bot_img = Image.open(BytesIO(bot_photo.getvalue())).convert("RGB")
                    bot_img = bot_img.resize((60, 60), Image.LANCZOS)
                    mask = Image.new('L', (66, 66), 0)
                    ImageDraw.Draw(mask).ellipse((0, 0, 66, 66), fill=255)
                    img.paste(bot_img, (550, 400), mask)
                    draw_text_with_shadow(620, 410, "Now Playing", font_event, (0, 255, 0))
            except Exception as e:
                logger.error(f"Bot profile error: {e}")

        # Requester profile image
        if requester_id:
            try:
                user = await app.get_users(requester_id)
                profile_photos = await app.get_profile_photos(requester_id, limit=1)
                if profile_photos:
                    photo = await app.download_media(profile_photos[0].file_id, in_memory=True)
                    user_img = Image.open(BytesIO(photo.getvalue())).convert("RGB")
                    user_img = user_img.resize((60, 60), Image.LANCZOS)
                    mask = Image.new('L', (66, 66), 0)
                    ImageDraw.Draw(mask).ellipse((0, 0, 66, 66), fill=255)
                    img.paste(user_img, (550, 460), mask)
                    draw_text_with_shadow(620, 470, "Requested by", font_event, (200, 200, 200))
                    draw_text_with_shadow(620, 500, f"{user.first_name[:12]}", font_event, (255, 255, 255))
            except Exception as e:
                logger.error(f"User profile error: {e}")

        # Footer elements
        draw_text_with_shadow(650, 550, datetime.now().strftime("%H:%M"), font_time, (200, 200, 200))
        draw.rounded_rectangle([40, 540, 120, 580], radius=10, fill=(100, 0, 0))
        draw_text_with_shadow(50, 550, "CLOSE", font_info, (255, 255, 255))

        thumb = BytesIO()
        img.save(thumb, "JPEG", quality=95)
        thumb.seek(0)
        
        await set_cached_data(cache_key, thumb.getvalue())
        return thumb

    except Exception as e:
        logger.error(f"Thumbnail error: {e}")
        # Fallback thumbnail
        img = Image.new("RGB", (800, 600), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((100, 300), title, fill=(255, 255, 255))
        thumb = BytesIO()
        img.save(thumb, "JPEG")
        thumb.seek(0)
        return thumb

# ======================
# MEDIA EXTRACTION
# ======================

async def extract_spotify_info(url: str) -> Optional[Union[Dict, List[Dict]]]:
    if not spotify:
        return None
    
    try:
        if 'track' in url:
            track = await asyncio.get_event_loop().run_in_executor(
                executor,
                lambda: spotify.track(url)
            )
            youtube_url = await get_youtube_url(f"{track['name']} {track['artists'][0]['name']}")
            if not youtube_url:
                return None
                
            return {
                'title': track['name'],
                'duration': track['duration_ms'] // 1000,
                'url': youtube_url,
                'thumbnail': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'artist': track['artists'][0]['name'],
                'source': 'spotify',
                'genre': track.get('genre', None)
            }
        elif 'playlist' in url:
            results = await asyncio.get_event_loop().run_in_executor(
                executor,
                lambda: spotify.playlist_tracks(url)
            )
            tracks = []
            for item in results['items']:
                track = item['track']
                youtube_url = await get_youtube_url(f"{track['name']} {track['artists'][0]['name']}")
                if youtube_url:
                    tracks.append({
                        'title': track['name'],
                        'duration': track['duration_ms'] // 1000,
                        'url': youtube_url,
                        'thumbnail': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'artist': track['artists'][0]['name'],
                        'source': 'spotify',
                        'genre': track.get('genre', None)
                    })
            return tracks if tracks else None
    except Exception as e:
        logger.error(f"Spotify error: {e}")
    return None

async def extract_m3u8_info(url: str) -> Optional[Dict]:
    try:
        return {
            'title': "M3U8 Stream",
            'duration': 0,
            'url': url,
            'thumbnail': None,
            'artist': "Live Stream",
            'source': 'm3u8',
            'is_live': True,
            'genre': 'live',
            'ffmpeg_options': get_ffmpeg_options(0)
        }
    except Exception as e:
        logger.error(f"M3U8 error: {e}")
    return None

async def extract_radio_info(url: str) -> Optional[Dict]:
    try:
        return {
            'title': "Live Radio Stream",
            'duration': 0,
            'url': url,
            'thumbnail': "https://i.imgur.com/JnPE5aN.png",  # Default radio icon
            'artist': "Live Radio",
            'source': 'radio',
            'is_live': True,
            'genre': 'radio',
            'ffmpeg_options': {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn -bufsize 1024k -content_type audio/mpeg'
            }
        }
    except Exception as e:
        logger.error(f"Radio stream error: {e}")
    return None

async def get_youtube_url(query: str) -> Optional[str]:
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': True,
        'noplaylist': True,
        'socket_timeout': 5,
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls']
            }
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.get_event_loop().run_in_executor(
                executor,
                lambda: ydl.extract_info(f"ytsearch:{query}", download=False)
            )
            if 'entries' in info and info['entries']:
                return info['entries'][0]['url']
    except Exception as e:
        logger.error(f"YouTube search error: {e}")
    return None

async def extract_info(query: str, audio_only: bool = True) -> Optional[Union[Dict, List[Dict]]]:
    try:
        # Handle radio stream URLs
        if any(x in query.lower() for x in ['radio.garden', 'radio-browser', '.pls', '.m3u', 'icecast', 'stream']):
            return await extract_radio_info(query)
        elif 'spotify' in query:
            return await extract_spotify_info(query)
        elif 'm3u8' in query.lower():
            return await extract_m3u8_info(query)
        else:
            ydl_opts = {
                'format': 'bestaudio/best' if audio_only else 'best',
                'quiet': True,
                'extract_flat': True,
                'noplaylist': True,
                'socket_timeout': 5,
                'extractor_args': {
                    'youtube': {
                        'skip': ['dash', 'hls']
                    }
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    lambda: ydl.extract_info(query, download=False)
                )
                if 'entries' in info:
                    info = info['entries'][0]
                
                return {
                    'title': info.get('title', 'Unknown Track'),
                    'duration': info.get('duration', 0),
                    'url': info['url'],
                    'thumbnail': info.get('thumbnail', None),
                    'artist': info.get('uploader', 'Unknown Artist'),
                    'source': 'youtube',
                    'is_video': not audio_only,
                    'genre': None
                }
    except Exception as e:
        logger.error(f"Error extracting info: {e}")
        return None

# ======================
# PLAYER CONTROL PANEL
# ======================

def create_player_ui(chat_id: int) -> Tuple[str, InlineKeyboardMarkup]:
    current_track = current_streams.get(chat_id, {})
    queue = queue_manager.queues.get(chat_id, [])
    
    text = f"""
🎵 **Now Playing** 🎵
┌ Title: {current_track.get('title', 'Nothing')}
├ Artist: {current_track.get('artist', 'Unknown')}
├ Duration: {format_duration(current_track.get('duration', 0))}
├ Source: {current_track.get('source', 'Unknown')}
└ Queue: {len(queue)} tracks waiting

🕒 {get_current_time()}
"""
    
    buttons = [
        [
            InlineKeyboardButton("⏮ Previous", callback_data="player_previous"),
            InlineKeyboardButton("⏸ Pause", callback_data="player_pause"),
            InlineKeyboardButton("⏭ Next", callback_data="player_next")
        ],
        [
            InlineKeyboardButton("🔁 Loop", callback_data="player_loop"),
            InlineKeyboardButton("🔀 Shuffle", callback_data="player_shuffle"),
            InlineKeyboardButton("🔊 Volume", callback_data="player_volume")
        ],
        [
            InlineKeyboardButton("📜 Queue", callback_data="player_queue"),
            InlineKeyboardButton("🛑 Stop", callback_data="player_stop")
        ],
        [
            InlineKeyboardButton("🎛 Close Panel", callback_data="player_close")
        ]
    ]
    
    return text, InlineKeyboardMarkup(buttons)

# ======================
# COMMAND INFO DISPLAY
# ======================

def format_command_info(command_type: str) -> str:
    detail = COMMAND_DETAILS[command_type]
    current_date = datetime.now().strftime("%B %d")
    text = f"# JhoomMusic\nbot\n\n"
    text += f"## {current_date}\n"
    text += f"JHOOM MUSIC\n\n"
    text += f"### INFO ABOUT COMMANDS\n\n"
    text += f"- **{detail['title']}**\n"
    text += "______\n"
    for cmd in detail['commands']:
        text += f"{cmd}\n"
    text += f"\n🕒 {get_current_time()}\n\n"
    text += "______\n\n"
    text += "### BACK\n\n"
    text += "JHOOM MUSIC\n\n"
    text += "### INFO ABOUT AI-FEATURES\n"
    return text

# ======================
# MAIN MENU
# ======================

def start_menu_ui() -> Tuple[str, InlineKeyboardMarkup]:
    current_time = get_current_time()
    text = f"""
🎵 **JHOOM MUSIC BOT**
HEY THERE, I'M JHOOM MUSIC - AN ADVANCED AI MUSIC PLAYER...

⚡ FEATURES:
• High-quality music streaming
• Supported platforms: YouTube, Spotify, M3U8
• Interactive player controls
• 24/7 playback support
• Multi-threaded performance
• Optimized FFmpeg configuration
• Self-repair capabilities

🕒 {current_time}
"""
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ADD TO GROUP", url=f"t.me/{app.me.username}?startgroup=true")],
        [
            InlineKeyboardButton("📜 HELP", callback_data="show_commands"),
            InlineKeyboardButton("🎛 PLAYER", callback_data="show_player")
        ],
        [
            InlineKeyboardButton("⚙️ SETTINGS", callback_data="settings_menu"),
            InlineKeyboardButton("⚙️ SYSTEM-UNIT", callback_data="system_info")
        ],
        [
            InlineKeyboardButton("🔧 QUICK FIX", callback_data="quick_fix_menu")
        ]
    ])
    return text, buttons

# ======================
# COMMANDS MENU
# ======================

def commands_menu_ui() -> Tuple[str, InlineKeyboardMarkup]:
    current_time = get_current_time()
    text = f"""
# JhoomMusic bot

## COMMANDS OF JHOOM MUSIC BOT

THERE ARE DIFFERENT TYPES OF COMMAND OF JHOOM MUSIC SOME OF THEM ARE ONLY FOR ADMINS AND SOME OF THEM ARE FOR ELITEUSERS.

- HOW TO USE COMMANDS?  
  - CLICK ON BUTTONS BELOW TO KNOW MORE.  
  - CHECK FEATURES LIKE ELITEUSERS ETC.  
  - / :- USE ALL FEATURES WITH THIS HANDLER.  

🕒 {current_time}
"""
    buttons = InlineKeyboardMarkup([
        [   
            InlineKeyboardButton("SULTAN", callback_data="cmd_sultan"),
            InlineKeyboardButton("LICENSE", callback_data="cmd_license"),
            InlineKeyboardButton("BROADCAST", callback_data="cmd_broadcast")
        ],
        [   
            InlineKeyboardButton("BL-CHAT", callback_data="cmd_blacklist"),
            InlineKeyboardButton("BL-USER", callback_data="cmd_block"),
            InlineKeyboardButton("CH-PLAY", callback_data="cmd_channel")
        ],
        [   
            InlineKeyboardButton("G-BANS", callback_data="cmd_gbans"),
            InlineKeyboardButton("SPIRAL", callback_data="cmd_spiral"),
            InlineKeyboardButton("REVAMP", callback_data="cmd_revamp")
        ],
        [   
            InlineKeyboardButton("PING", callback_data="cmd_ping"),
            InlineKeyboardButton("PLAY", callback_data="cmd_play"),
            InlineKeyboardButton("SHUFFLE", callback_data="cmd_shuffle")
        ],
        [   
            InlineKeyboardButton("SEEK", callback_data="cmd_seek"),
            InlineKeyboardButton("SONG", callback_data="cmd_song"),
            InlineKeyboardButton("SPEED", callback_data="cmd_speed")
        ],
        [   
            InlineKeyboardButton("VIDEO", callback_data="cmd_vplay"),
            InlineKeyboardButton("QUEUE", callback_data="cmd_queue")
        ],
        [   
            InlineKeyboardButton("REPAIR", callback_data="cmd_troubleshoot"),
            InlineKeyboardButton("RADIO", callback_data="cmd_radio")
        ],
        [   
            InlineKeyboardButton("🔙 BACK", callback_data="back_to_start")
        ]
    ])
    return text, buttons

# ======================
# QUICK FIX MENU
# ======================

def quick_fix_menu_ui() -> Tuple[str, InlineKeyboardMarkup]:
    current_time = get_current_time()
    text = f"""
# JhoomMusic  
bot  

## {datetime.now().strftime('%B %d')}  
JHOOM MUSIC  

IF YOU WANT MORE INFORMATION ABOUT ME THEN CHECK THE BELOW BUTTONS !!  

- **PYROGRAM VERSION** = 2.0.106  
- **JHOOM MUSIC VERSION** = 1.0  
- **FFMPEG PROCESSES** = {FFMPEG_PROCESSES}  
- **SELF-REPAIR SYSTEM** = ACTIVE  

🕒 {current_time}
"""
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🆘 SUPPORT", url="https://t.me/JhoomMusicSupport")],
        [InlineKeyboardButton("🔄 UPDATES", url="https://t.me/JhoomMusicUpdates")],
        [InlineKeyboardButton("⚙️ SYSTEM-UNIT", callback_data="system_info")],
        [InlineKeyboardButton("🔧 RUN DIAGNOSTICS", callback_data="run_diagnostics")],
        [InlineKeyboardButton("🔙 BACK", callback_data="back_to_start")]
    ])
    return text, buttons

# ======================
# SETTINGS MENU
# ======================

def settings_menu_ui(chat_id: int) -> Tuple[str, InlineKeyboardMarkup]:
    current_time = get_current_time()
    text = f"""
⚙️ **JHOOM MUSIC SETTINGS**

CUSTOMIZE YOUR BOT EXPERIENCE WITH THESE OPTIONS:

• Volume: 100%
• Quality: High
• Language: English
• Notifications: On

🕒 {current_time}
"""
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔊 Volume", callback_data=f"settings_volume_{chat_id}")],
        [InlineKeyboardButton("🎚 Quality", callback_data=f"settings_quality_{chat_id}")],
        [InlineKeyboardButton("🌐 Language", callback_data=f"settings_lang_{chat_id}")],
        [InlineKeyboardButton("🔔 Notifications", callback_data=f"settings_notify_{chat_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
    ])
    return text, buttons

# ======================
# CACHE FUNCTIONS
# ======================

async def get_cached_data(key: str) -> Optional[Any]:
    if not redis_client:
        return None
    
    try:
        data = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: redis_client.get(key)
        )
        return json.loads(data) if data else None
    except Exception as e:
        logger.error(f"Cache get error: {e}")
        return None

async def set_cached_data(key: str, data: Any, expire: int = 3600) -> None:
    if not redis_client:
        return
    
    try:
        await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: redis_client.setex(key, expire, json.dumps(data))
        )
    except Exception as e:
        logger.error(f"Cache set error: {e}")

# ======================
# PLAYER CONTROL COMMANDS
# ======================

@app.on_message(filters.command(["player", "control"]))
async def show_player_panel(_, message: Message):
    chat_id = message.chat.id
    if chat_id not in current_streams:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ No active playback to control"
        )
        return
    
    text, buttons = create_player_ui(chat_id)
    await message.reply_photo(
        photo=UI_IMAGES["player"],
        caption=text,
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("^show_player$"))
async def show_player_menu(_, query: CallbackQuery):
    chat_id = query.message.chat.id
    if chat_id not in current_streams:
        await query.answer("No active playback", show_alert=True)
        return
    
    text, buttons = create_player_ui(chat_id)
    await query.message.edit_media(
        media=InputMediaPhoto(UI_IMAGES["player"]),
        caption=text,
        reply_markup=buttons
    )
    await query.answer()

@app.on_callback_query(filters.regex("^player_"))
async def handle_player_controls(_, query: CallbackQuery):
    chat_id = query.message.chat.id
    action = query.data.split("_")[1]
    
    if chat_id not in current_streams:
        await query.answer("No active playback", show_alert=True)
        return
    
    if action == "pause":
        await pytgcalls.pause_stream(chat_id)
        await query.answer("Playback paused")
    elif action == "resume":
        await pytgcalls.resume_stream(chat_id)
        await query.answer("Playback resumed")
    elif action == "next":
        await play_next_track(chat_id)
        await query.answer("Skipping to next track")
    elif action == "previous":
        await query.answer("Previous track not implemented yet")
    elif action == "loop":
        loop_status[chat_id] = {'type': 'track', 'count': 3}
        await query.answer("Loop enabled (3 times)")
    elif action == "shuffle":
        if chat_id in queue_manager.queues and queue_manager.queues[chat_id]:
            random.shuffle(queue_manager.queues[chat_id])
            shuffle_status[chat_id] = True
            await query.answer("Queue shuffled")
        else:
            await query.answer("No tracks in queue to shuffle", show_alert=True)
    elif action == "volume":
        await query.answer("Volume control not implemented yet")
    elif action == "queue":
        if chat_id in queue_manager.queues and queue_manager.queues[chat_id]:
            queue_text = "🎧 Queue:\n\n" + "\n".join(
                f"{i+1}. {track['title']}" 
                for i, track in enumerate(queue_manager.queues[chat_id][:10])
            )
            await query.answer(queue_text, show_alert=True)
        else:
            await query.answer("Queue is empty", show_alert=True)
    elif action == "stop":
        await connection_manager.release_connection(chat_id)
        if chat_id in current_streams:
            del current_streams[chat_id]
        await queue_manager.clear_queue(chat_id)
        await query.answer("Playback stopped")
    elif action == "close":
        await query.message.delete()
        return
    
    text, buttons = create_player_ui(chat_id)
    await query.message.edit_media(
        media=InputMediaPhoto(UI_IMAGES["player"]),
        caption=text,
        reply_markup=buttons
    )

# ======================
# MAIN COMMAND HANDLERS
# ======================

@app.on_message(filters.command(["play", "p"]))
async def play_music(_, message: Message):
    if await is_user_gbanned(message.from_user.id):
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="🚫 You are banned from using this bot."
        )
        return
        
    if not await check_user_auth(message.from_user.id):
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="🔒 You need to be authorized to use this command."
        )
        return

    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="Usage: /play [song name or URL] or reply to an audio file"
        )
        return
    
    query = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    chat_id = message.chat.id
    
    if message.reply_to_message and (message.reply_to_message.audio or message.reply_to_message.video):
        file = message.reply_to_message.audio or message.reply_to_message.video
        track = {
            'title': file.title or file.file_name,
            'artist': 'Telegram Media',
            'duration': file.duration or 0,
            'url': await app.download_media(file),
            'source': 'telegram',
            'is_video': bool(message.reply_to_message.video),
            'user_id': message.from_user.id,
            'genre': None
        }
    else:
        track_info = await extract_info(query)
        if not track_info:
            await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption="❌ Could not find the requested track"
            )
            return
        
        if isinstance(track_info, list):
            for t in track_info:
                t['user_id'] = message.from_user.id
        else:
            track_info['user_id'] = message.from_user.id
    
    if isinstance(track_info, list):
        if not track_info:
            await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption="❌ No tracks found in playlist"
            )
            return
            
        if chat_id in current_streams:
            await queue_manager.add_to_queue(chat_id, track_info[0])
            if len(track_info) > 1:
                for t in track_info[1:]:
                    await queue_manager.add_to_queue(chat_id, t)
            
            await message.reply_photo(
                photo=UI_IMAGES["success"],
                caption=f"🎧 Added {len(track_info)} tracks to queue"
            )
        else:
            current_streams[chat_id] = track_info[0]
            if len(track_info) > 1:
                for t in track_info[1:]:
                    await queue_manager.add_to_queue(chat_id, t)
            
            await play_next_track(chat_id)
            await message.reply_photo(
                photo=UI_IMAGES["success"],
                caption=f"▶️ Now Playing: {track_info[0]['title']}"
            )
        return
    
    thumb = await generate_advanced_music_thumbnail(
        title=track_info['title'],
        channel=track_info.get('artist', 'Unknown Artist'),
        views=track_info.get('views', '0 views'),
        duration=str(timedelta(seconds=track_info.get('duration', 0)))),
        current_time="00:00",
        query_by=message.from_user.first_name,
        cover_url=track_info.get('thumbnail'),
        bot_user_id=app.me.id,
        requester_id=message.from_user.id,
        progress_percentage=0.0
    )
    
    if chat_id in current_streams:
        await queue_manager.add_to_queue(chat_id, track_info)
        await message.reply_photo(
            photo=thumb,
            caption=f"🎧 Added to queue: {track_info['title']}"
        )
    else:
        current_streams[chat_id] = track_info
        await play_next_track(chat_id)
        await message.reply_photo(
            photo=thumb,
            caption=f"▶️ Now Playing: {track_info['title']}"
        )

@app.on_message(filters.command(["vplay", "vp"]))
async def video_play(_, message: Message):
    if await is_user_gbanned(message.from_user.id):
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="🚫 You are banned from using this bot."
        )
        return
        
    if not await check_user_auth(message.from_user.id):
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="🔒 You need to be authorized to use this command."
        )
        return

    if len(message.command) < 2:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="Usage: /vplay [video name or URL]"
        )
        return
    
    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    
    video_info = await extract_info(query, audio_only=False)
    if not video_info:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ Could not find the requested video"
        )
        return
    
    video_info['is_video'] = True
    video_info['user_id'] = message.from_user.id
    
    thumb = await generate_advanced_music_thumbnail(
        title=video_info['title'],
        channel=video_info.get('artist', 'Unknown Artist'),
        views=video_info.get('views', '0 views'),
        duration=str(timedelta(seconds=video_info.get('duration', 0)))),
        current_time="00:00",
        query_by=message.from_user.first_name,
        cover_url=video_info.get('thumbnail'),
        bot_user_id=app.me.id,
        requester_id=message.from_user.id,
        progress_percentage=0.0
    )
    
    if chat_id in current_streams:
        await queue_manager.add_to_queue(chat_id, video_info)
        await message.reply_photo(
            photo=thumb,
            caption=f"🎬 Added to queue: {video_info['title']}"
        )
    else:
        current_streams[chat_id] = video_info
        await play_next_track(chat_id)
        await message.reply_photo(
            photo=thumb,
            caption=f"🎬 Now Playing: {video_info['title']}"
        )

# ======================
# PLAYBACK CONTROLS
# ======================

@app.on_message(filters.command(["pause", "pa"]))
async def pause_music(_, message: Message):
    chat_id = message.chat.id
    try:
        await pytgcalls.pause_stream(chat_id)
        await message.reply_photo(
            photo=UI_IMAGES["sultan"],
            caption="⏸ Playback paused"
        )
    except Exception as e:
        logger.error(f"Pause error in chat {chat_id}: {e}")
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ No active playback to pause"
        )

@app.on_message(filters.command(["resume", "r"]))
async def resume_music(_, message: Message):
    chat_id = message.chat.id
    try:
        await pytgcalls.resume_stream(chat_id)
        await message.reply_photo(
            photo=UI_IMAGES["sultan"],
            caption="▶️ Playback resumed"
        )
    except Exception as e:
        logger.error(f"Resume error in chat {chat_id}: {e}")
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ No paused playback"
        )

@app.on_message(filters.command(["skip", "s"]))
async def skip_music(_, message: Message):
    chat_id = message.chat.id
    if chat_id in current_streams:
        await play_next_track(chat_id)
        await message.reply_photo(
            photo=UI_IMAGES["sultan"],
            caption="⏭ Skipped to next track"
        )
    else:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ No active playback"
        )

@app.on_message(filters.command(["stop", "st"]))
async def stop_music(_, message: Message):
    chat_id = message.chat.id
    if chat_id in current_streams:
        await connection_manager.release_connection(chat_id)
        del current_streams[chat_id]
        await queue_manager.clear_queue(chat_id)
        await message.reply_photo(
            photo=UI_IMAGES["sultan"],
            caption="⏹ Playback stopped"
        )
    else:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ No active playback"
        )

# ======================
# ADVANCED PLAYBACK CONTROLS
# ======================

@app.on_message(filters.command(["loop", "spiral"]))
async def loop_control(_, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="Usage: /loop [enable/disable/track/queue] or [1-10]"
        )
        return
    
    arg = message.command[1].lower()
    
    if arg == "enable" or arg == "track":
        loop_status[chat_id] = {'type': 'track', 'count': 1}
        await message.reply_photo(
            photo=UI_IMAGES["spiral"],
            caption="🔁 Track loop enabled (1 time)"
        )
    elif arg == "queue":
        loop_status[chat_id] = {'type': 'queue', 'count': 1}
        await message.reply_photo(
            photo=UI_IMAGES["spiral"],
            caption="🔁 Queue loop enabled"
        )
    elif arg == "disable":
        loop_status.pop(chat_id, None)
        await message.reply_photo(
            photo=UI_IMAGES["spiral"],
            caption="🔁 Loop disabled"
        )
    elif arg.isdigit() and 1 <= int(arg) <= 10:
        if chat_id in loop_status:
            loop_status[chat_id]['count'] = int(arg)
        else:
            loop_status[chat_id] = {'type': 'track', 'count': int(arg)}
        await message.reply_photo(
            photo=UI_IMAGES["spiral"],
            caption=f"🔁 Loop set to {arg} times"
        )
    else:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ Invalid loop command"
        )

@app.on_message(filters.command("shuffle"))
async def shuffle_queue(_, message: Message):
    chat_id = message.chat.id
    if chat_id in queue_manager.queues and queue_manager.queues[chat_id]:
        random.shuffle(queue_manager.queues[chat_id])
        shuffle_status[chat_id] = True
        await message.reply_photo(
            photo=UI_IMAGES["shuffle"],
            caption="🔀 Queue shuffled"
        )
    else:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ No tracks in queue to shuffle"
        )

@app.on_message(filters.command(["seek", "seekback"]))
async def seek_track(_, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2 or chat_id not in current_streams:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="Usage: /seek [seconds]"
        )
        return
    try:
        seconds = int(message.command[1])
        track = current_streams[chat_id]
        await pytgcalls.change_stream(
            chat_id,
            AudioPiped(track['url'], HighQualityAudio(), seek=seconds)
        )
        await message.reply_photo(
            photo=UI_IMAGES["seek"],
            caption=f"⏩ Seeked to {seconds} seconds"
        )
    except Exception as e:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption=f"❌ Seek error: {e}"
        )

# ======================
# PLAYLIST MANAGEMENT
# ======================

@app.on_message(filters.command(["playlist", "pl"]))
async def playlist_management(_, message: Message):
    if len(message.command) < 2:
        user_playlists = await playlists.find({"user_id": message.from_user.id}).to_list(None)
        if not user_playlists:
            await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption="You don't have any playlists yet. Create one with /playlist create [name]"
            )
            return
        
        text = "🎵 Your Playlists:\n\n"
        for pl in user_playlists:
            text += f"- {pl['name']} ({len(pl['tracks'])} tracks)\n"
        
        buttons = []
        for pl in user_playlists[:5]:
            buttons.append([
                InlineKeyboardButton(
                    f"▶️ {pl['name']}",
                    callback_data=f"play_pl_{pl['_id']}"
                )
            ])
            buttons.append([
                InlineKeyboardButton(
                    f"🗑 Delete {pl['name']}",
                    callback_data=f"del_pl_{pl['_id']}"
                )
            ])
        
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_start")])
        
        await message.reply_photo(
            photo=UI_IMAGES["playlist"],
            caption=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    
    subcmd = message.command[1].lower()
    
    if subcmd == "create" and len(message.command) > 2:
        pl_name = " ".join(message.command[2:])
        await playlists.insert_one({
            "user_id": message.from_user.id,
            "name": pl_name,
            "tracks": []
        })
        await message.reply_photo(
            photo=UI_IMAGES["success"],
            caption=f"✅ Playlist '{pl_name}' created"
        )
    
    elif subcmd == "add" and len(message.command) > 3:
        pl_name = message.command[2]
        query = " ".join(message.command[3:])
        
        track = await extract_info(query)
        if not track:
            await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption="❌ Could not find the track"
            )
            return
        
        await playlists.update_one(
            {"user_id": message.from_user.id, "name": pl_name},
            {"$push": {"tracks": track}}
        )
        await message.reply_photo(
            photo=UI_IMAGES["success"],
            caption=f"✅ Added to playlist '{pl_name}'"
        )
    
    elif subcmd == "play" and len(message.command) > 2:
        pl_name = " ".join(message.command[2:])
        playlist = await playlists.find_one({
            "user_id": message.from_user.id,
            "name": pl_name
        })
        
        if not playlist:
            await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption=f"❌ Playlist '{pl_name}' not found"
            )
            return
        
        chat_id = message.chat.id
        if chat_id in current_streams:
            await queue_manager.add_to_queue(chat_id, playlist['tracks'][0])
            if len(playlist['tracks']) > 1:
                for t in playlist['tracks'][1:]:
                    await queue_manager.add_to_queue(chat_id, t)
            
            await message.reply_photo(
                photo=UI_IMAGES["success"],
                caption=f"🎧 Added {len(playlist['tracks'])} tracks from '{pl_name}' to queue"
            )
        else:
            current_streams[chat_id] = playlist['tracks'][0]
            if len(playlist['tracks']) > 1:
                for t in playlist['tracks'][1:]:
                    await queue_manager.add_to_queue(chat_id, t)
            
            await play_next_track(chat_id)
            await message.reply_photo(
                photo=UI_IMAGES["success"],
                caption=f"▶️ Playing playlist '{pl_name}'"
            )

# ======================
# ADMIN COMMANDS
# ======================

@app.on_message(filters.command("auth") & filters.user(SUDO_USERS))
async def auth_user(_, message: Message):
    if len(message.command) < 2:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="Usage: /auth user_id"
        )
        return
    
    try:
        user_id = int(message.command[1])
        await auth_users.insert_one({"user_id": user_id})
        await message.reply_photo(
            photo=UI_IMAGES["license"],
            caption=f"✅ User {user_id} added to auth list"
        )
    except ValueError:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ Invalid user ID"
        )

@app.on_message(filters.command("unauth") & filters.user(SUDO_USERS))
async def unauth_user(_, message: Message):
    if len(message.command) < 2:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="Usage: /unauth user_id"
        )
        return
    
    try:
        user_id = int(message.command[1])
        result = await auth_users.delete_one({"user_id": user_id})
        if result.deleted_count > 0:
            await message.reply_photo(
                photo=UI_IMAGES["license"],
                caption=f"✅ User {user_id} removed from auth list"
            )
        else:
            await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption=f"❌ User {user_id} not found in auth list"
            )
    except ValueError:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ Invalid user ID"
        )

@app.on_message(filters.command("authusers") & filters.user(SUDO_USERS))
async def show_auth_users(_, message: Message):
    auth_users_list = await auth_users.find().to_list(None)
    if not auth_users_list:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="No authorized users found"
        )
        return
    
    text = "🔐 Authorized Users:\n\n"
    for user in auth_users_list:
        text += f"- User ID: {user['user_id']}\n"
    
    await message.reply_photo(
        photo=UI_IMAGES["license"],
        caption=text
    )

@app.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast_message(_, message: Message):
    if len(message.command) < 2:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="Usage: /broadcast [-options] message"
        )
        return
    
    parts = message.text.split()
    options = [p for p in parts if p.startswith('-')]
    broadcast_msg = ' '.join([p for p in parts if not p.startswith('-')][1:])
    
    all_chats = await chats.find().to_list(None)
    
    if not all_chats:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ No chats found to broadcast"
        )
        return
    
    pin_message = '-pin' in options
    notify = '-pinloud' in options
    to_users = '-user' in options
    from_assistant = '-assistant' in options
    no_bot = '-nobot' in options
    
    success = 0
    failed = 0
    total = len(all_chats)
    
    progress = await message.reply_photo(
        photo=UI_IMAGES["broadcast"],
        caption=f"📢 Starting broadcast to {total} chats..."
    )
    
    for chat in all_chats:
        try:
            if to_users and chat['chat_id'] > 0:
                await app.send_message(
                    chat['chat_id'],
                    broadcast_msg
                )
                success += 1
            elif not to_users and chat['chat_id'] < 0:
                await app.send_message(
                    chat['chat_id'],
                    broadcast_msg
                )
                success += 1
                
            if pin_message:
                try:
                    if chat['chat_id'] < 0:
                        last_msg = await app.get_history(chat['chat_id'], limit=1)
                        if last_msg:
                            await app.pin_chat_message(
                                chat['chat_id'],
                                last_msg[0].message_id,
                                disable_notification=not notify
                            )
                except Exception as e:
                    logger.error(f"Error pinning message in {chat['chat_id']}: {e}")
            
            if (success + failed) % 10 == 0:
                await progress.edit_caption(
                    caption=f"📢 Broadcasting...\nSuccess: {success}\nFailed: {failed}\nRemaining: {total - success - failed}"
                )
        except Exception as e:
            logger.error(f"Error broadcasting to {chat['chat_id']}: {e}")
            failed += 1
    
    await progress.edit_caption(
        caption=f"📢 Broadcast completed!\nSuccess: {success}\nFailed: {failed}"
    )

@app.on_message(filters.command(["gban", "globalban"]) & filters.user(SUDO_USERS))
async def global_ban_user(_, message: Message):
    if len(message.command) < 2:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="Usage: /gban user_id [reason]"
        )
        return
    
    try:
        user_id = int(message.command[1])
        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided"
        
        await gbanned_users.update_one(
            {"user_id": user_id},
            {"$set": {"reason": reason, "banned_by": message.from_user.id, "banned_at": datetime.utcnow()}},
            upsert=True
        )
        
        await message.reply_photo(
            photo=UI_IMAGES["gbans"],
            caption=f"🔨 User {user_id} has been globally banned\nReason: {reason}"
        )
    except ValueError:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ Invalid user ID"
        )

@app.on_message(filters.command(["ungban", "unglobalban"]) & filters.user(SUDO_USERS))
async def global_unban_user(_, message: Message):
    if len(message.command) < 2:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="Usage: /ungban user_id"
        )
        return
    
    try:
        user_id = int(message.command[1])
        result = await gbanned_users.delete_one({"user_id": user_id})
        
        if result.deleted_count > 0:
            await message.reply_photo(
                photo=UI_IMAGES["gbans"],
                caption=f"✅ User {user_id} has been globally unbanned"
            )
        else:
            await message.reply_photo(
                photo=UI_IMAGES["error"],
                caption=f"❌ User {user_id} was not globally banned"
            )
    except ValueError:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="❌ Invalid user ID"
        )

@app.on_message(filters.command(["gbannedusers", "globalbans"]) & filters.user(SUDO_USERS))
async def show_global_bans(_, message: Message):
    banned_users = await gbanned_users.find().to_list(None)
    
    if not banned_users:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption="No users are currently globally banned"
        )
        return
    
    text = "🔨 Globally Banned Users:\n\n"
    for user in banned_users:
        text += f"• User ID: {user['user_id']}\n"
        text += f"  Reason: {user.get('reason', 'Not specified')}\n"
        text += f"  Banned by: {user.get('banned_by', 'Unknown')}\n"
        text += f"  Date: {user.get('banned_at', 'Unknown').strftime('%Y-%m-%d') if 'banned_at' in user else 'Unknown'}\n\n"
    
    await message.reply_photo(
        photo=UI_IMAGES["gbans"],
        caption=text
    )

@app.on_message(filters.command(["logs", "log"]) & filters.user(SUDO_USERS))
async def send_logs(_, message: Message):
    try:
        await message.reply_document(
            document="jhoommusic.log",
            caption="📜 Bot logs"
        )
    except Exception as e:
        await message.reply_photo(
            photo=UI_IMAGES["error"],
            caption=f"❌ Error sending logs: {e}"
        )

@app.on_message(filters.command(["ping", "speed"]) & filters.group)
async def ping_pong(_, message: Message):
    start = time.time()
    msg = await message.reply_photo(
        photo=UI_IMAGES["ping"],
        caption="🏓 Pong!"
    )
    end = time.time()
    await msg.edit_caption(
        caption=f"🏓 Pong!\n⏱ Response time: {(end - start) * 1000:.2f} ms"
    )

@app.on_message(filters.command(["uptime", "up"]) & filters.group)
async def show_uptime(_, message: Message):
    await message.reply_photo(
        photo=UI_IMAGES["ping"],
        caption=f"⏱ Bot Uptime: {get_uptime()}"
    )

# ======================
# SETTINGS COMMANDS
# ======================

@app.on_message(filters.command("settings"))
async def settings_command(_, message: Message):
    chat_id = message.chat.id
    text, buttons = settings_menu_ui(chat_id)
    await message.reply_photo(
        photo=UI_IMAGES["settings"],
        caption=text,
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("^settings_"))
async def handle_settings(_, query: CallbackQuery):
    action, chat_id = query.data.split("_")[1:]
    chat_id = int(chat_id)
    
    if action == "volume":
        await query.answer("Volume control coming soon", show_alert=True)
    elif action == "quality":
        await query.answer("Quality settings coming soon", show_alert=True)
    elif action == "lang":
        await query.answer("Language settings coming soon", show_alert=True)
    elif action == "notify":
        await query.answer("Notification settings coming soon", show_alert=True)
    
    # Return to settings menu
    text, buttons = settings_menu_ui(chat_id)
    await query.message.edit_media(
        media=InputMediaPhoto(UI_IMAGES["settings"]),
        caption=text,
        reply_markup=buttons
    )

# ======================
# UI HANDLERS
# ======================

@app.on_message(filters.command("start"))
async def start_command(_, msg: Message):
    text, buttons = start_menu_ui()
    await msg.reply_photo(
        photo=UI_IMAGES["main_menu"],
        caption=text,
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("^show_commands$"))
async def show_commands_menu(_, query: CallbackQuery):
    text, buttons = commands_menu_ui()
    await query.message.edit_media(
        media=InputMediaPhoto(UI_IMAGES["commands_menu"]),
        caption=text,
        reply_markup=buttons
    )
    await query.answer()

@app.on_callback_query(filters.regex("^cmd_"))
async def show_command_info(_, query: CallbackQuery):
    command_type = query.data.split("_")[1]
    if command_type in COMMAND_DETAILS:
        text = format_command_info(command_type)
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 BACK", callback_data="show_commands")]
        ])
        await query.message.edit_media(
            media=InputMediaPhoto(UI_IMAGES["commands_menu"]),
            caption=text,
            reply_markup=buttons
        )
    await query.answer()

@app.on_callback_query(filters.regex("^quick_fix_menu$"))
async def show_quick_fix_menu(_, query: CallbackQuery):
    text, buttons = quick_fix_menu_ui()
    await query.message.edit_media(
        media=InputMediaPhoto(UI_IMAGES["diagnostics"]),
        caption=text,
        reply_markup=buttons
    )
    await query.answer()

@app.on_callback_query(filters.regex("^system_info$"))
async def show_system_info(_, query: CallbackQuery):
    system_status = await get_system_status()
    await query.message.edit_media(
        media=InputMediaPhoto(UI_IMAGES["admin"]),
        caption=system_status,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="system_info")],
            [InlineKeyboardButton("🔙 BACK", callback_data="back_to_start")]
        ])
    )
    await query.answer()

@app.on_callback_query(filters.regex("^run_diagnostics$"))
async def run_diagnostics_callback(_, query: CallbackQuery):
    chat_id = query.message.chat.id
    report = await run_diagnostics(chat_id)
    await query.message.edit_media(
        media=InputMediaPhoto(UI_IMAGES["diagnostics"]),
        caption=report,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Run Again", callback_data="run_diagnostics")],
            [InlineKeyboardButton("🔙 BACK", callback_data="quick_fix_menu")]
        ])
    )
    await query.answer()

@app.on_callback_query(filters.regex("^play_pl_"))
async def play_playlist_callback(_, query: CallbackQuery):
    playlist_id = query.data.split("_")[2]
    playlist = await playlists.find_one({"_id": playlist_id})
    
    if not playlist:
        await query.answer("Playlist not found", show_alert=True)
        return
    
    chat_id = query.message.chat.id
    if chat_id in current_streams:
        await queue_manager.add_to_queue(chat_id, playlist['tracks'][0])
        if len(playlist['tracks']) > 1:
            for t in playlist['tracks'][1:]:
                await queue_manager.add_to_queue(chat_id, t)
        
        await query.message.reply_photo(
            photo=UI_IMAGES["success"],
            caption=f"🎧 Added {len(playlist['tracks'])} tracks to queue"
        )
    else:
        current_streams[chat_id] = playlist['tracks'][0]
        if len(playlist['tracks']) > 1:
            for t in playlist['tracks'][1:]:
                await queue_manager.add_to_queue(chat_id, t)
        
        await play_next_track(chat_id)
        await query.message.reply_photo(
            photo=UI_IMAGES["success"],
            caption=f"▶️ Playing playlist '{playlist['name']}'"
        )
    
    await query.answer()

@app.on_callback_query(filters.regex("^del_pl_"))
async def delete_playlist_callback(_, query: CallbackQuery):
    playlist_id = query.data.split("_")[2]
    result = await playlists.delete_one({"_id": playlist_id})
    
    if result.deleted_count > 0:
        await query.answer("Playlist deleted", show_alert=True)
        await show_commands_menu(_, query)
    else:
        await query.answer("Failed to delete playlist", show_alert=True)

@app.on_callback_query(filters.regex("^back_to_start$"))
async def back_to_start(_, query: CallbackQuery):
    text, buttons = start_menu_ui()
    await query.message.edit_media(
        media=InputMediaPhoto(UI_IMAGES["main_menu"]),
        caption=text,
        reply_markup=buttons
    )
    await query.answer()

# ======================
# PARTICIPANT HANDLING
# ======================

@pytgcalls.on_participant_change()
async def on_participant_change(client: PyTgCalls, update: Update):
    chat_id = update.chat_id
    participants = await pytgcalls.get_participants(chat_id)
    if len(participants) <= 1:
        await connection_manager.release_connection(chat_id)
        if chat_id in current_streams:
            del current_streams[chat_id]
        await app.send_photo(
            chat_id, 
            UI_IMAGES["error"], 
            caption="⏹ Stopped due to no listeners"
        )

# ======================
# TELEGRAM MEDIA PLAYBACK
# ======================

@app.on_message(filters.command("play") & filters.group)
async def play_telegram_media(_, message: Message):
    if message.reply_to_message and (message.reply_to_message.audio or message.reply_to_message.video):
        file = message.reply_to_message.audio or message.reply_to_message.video
        track = {
            'title': file.title or file.file_name,
            'artist': 'Telegram Media',
            'duration': file.duration or 0,
            'url': await app.download_media(file),
            'source': 'telegram',
            'is_video': bool(message.reply_to_message.video),
            'user_id': message.from_user.id,
            'genre': None
        }
        
        chat_id = message.chat.id
        if chat_id in current_streams:
            await queue_manager.add_to_queue(chat_id, track)
            await message.reply_photo(
                photo=UI_IMAGES["success"],
                caption=f"🎧 Added to queue: {track['title']}"
            )
        else:
            current_streams[chat_id] = track
            await play_next_track(chat_id)
            await message.reply_photo(
                photo=UI_IMAGES["success"],
                caption=f"▶️ Now Playing: {track['title']}"
            )

# ======================
# MUSIC ENGINE
# ======================

MUSIC_APIS = [
    {"name": "JioSaavn", "url": "https://saavn.dev/api/search/songs", "auth": False},
    {"name": "Invidious Puffyan", "url": "https://vid.puffyan.us/api/v1/search", "auth": False},
    {"name": "Invidious Yewtu", "url": "https://yewtu.be/api/v1/search", "auth": False},
    {"name": "Invidious Segfault", "url": "https://invidious.projectsegfau.lt/api/v1/search", "auth": False},
    {"name": "Deezer", "url": "https://api.deezer.com/search", "auth": False},
    {"name": "SoundCloud", "url": "https://api-v2.soundcloud.com/search/tracks", "auth": False},
]

async def search_song(query: str) -> Dict:
    """Search for a song using multiple APIs with fallback"""
    for api in MUSIC_APIS:
        try:
            if "saavn" in api["url"]:
                response = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    lambda: requests.get(api["url"], params={"query": query})
                )
            elif "deezer" in api["url"]:
                response = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    lambda: requests.get(api["url"], params={"q": query})
                )
            elif "soundcloud" in api["url"]:
                response = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    lambda: requests.get(api["url"], params={"q": query})
                )
            else:
                response = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    lambda: requests.get(api["url"], params={"q": query})
                )

            if response.status_code == 200:
                data = response.json()
                return {
                    "source": api["name"],
                    "data": data
                }
        except Exception as e:
            logger.error(f"[ERROR] {api['name']} failed: {e}")
            continue
    
    return {"error": "No API responded successfully."}

# ======================
# STARTUP AND MAINTENANCE
# ======================

async def periodic_maintenance():
    while True:
        try:
            await check_all_groups_health()
            await process_manager.adjust_processes()
            await asyncio.sleep(300)  # Run every 5 minutes
        except Exception as e:
            logger.error(f"Maintenance error: {e}")

@app.on_raw_update()
async def on_startup():
    logger.info("Bot started successfully!")
    await app.send_photo(
        SUPER_GROUP_ID,
        UI_IMAGES["startup"],
        caption="⚡ Jhoom Music Bot is now online!\n"
        f"Uptime: {get_uptime()}\n"
        f"Version: 1.0"
    )
    asyncio.create_task(periodic_maintenance())

# ======================
# RUN THE BOT
# ======================

if __name__ == "__main__":
    print("🎵 Jhoom Music Bot is starting...")
    try:
        pytgcalls.start()
        app.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        exit(1)