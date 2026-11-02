"""
JhoomMusic package initialization.
Only creates the bot and userbot clients.
All other setup is done in main.py
"""

import sys
from pyrogram import Client

import config
from .logging import LOGGER

# -------------------- Validate required config --------------------
if not all([config.API_ID, config.API_HASH, config.BOT_TOKEN]):
    LOGGER(__name__).error("API_ID, API_HASH or BOT_TOKEN is missing in .env")
    sys.exit(1)

# -------------------- Main Bot Client --------------------
app = Client(
    name="JhoomMusic",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

# -------------------- Userbot / Assistant Client --------------------
if config.STRING_SESSION:
    userbot = Client(
        name="JhoomMusicAssistant",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.STRING_SESSION,
    )
else:
    userbot = None
    LOGGER(__name__).warning("STRING_SESSION not found → Userbot disabled")

LOGGER(__name__).info("JhoomMusic clients created successfully")
