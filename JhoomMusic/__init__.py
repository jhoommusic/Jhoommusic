import sys
import time
import logging
from pyrogram import Client
from pytgcalls import PyTgCalls

import config

# Configure logging
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)

LOGGER = logging.getLogger

# Initialize main bot
if config.API_ID and config.API_HASH and config.BOT_TOKEN:
    app = Client(
        "JhoomMusic",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN,
    )
else:
    LOGGER(__name__).error("API_ID, API_HASH or BOT_TOKEN not found")
    sys.exit()

# Initialize userbot
if config.STRING_SESSION:
    userbot = Client(
        "JhoomMusicAssistant",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.STRING_SESSION,
    )
else:
    userbot = None
    LOGGER(__name__).warning("STRING_SESSION not found, userbot disabled")

# Import core modules
from .core.bot import JhoomBot
from .core.dir import dirr
from .core.git import git
from .core.userbot import Userbot
from .misc import dbb, heroku, sudo

# Initialize directories and database
dirr()
git()
dbb()
heroku()
sudo()

# Set bot username
app.username = config.BOT_USERNAME

LOGGER(__name__).info("JhoomMusic Bot Initialized Successfully")