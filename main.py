from dotenv import load_dotenv
load_dotenv()

import asyncio
import logging
from JhoomMusic import app, userbot
from JhoomMusic.core.call import Jhoom
from JhoomMusic.misc import sudo
from JhoomMusic.plugins import ALL_MODULES
import importlib

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


async def init():
    """Initialize the bot"""

async def init():
    """Initialize the bot"""
    try:
        # Initialize sudo users
        await sudo()

        # Start the main bot
        await app.start()

        # Import all plugins
        for module in ALL_MODULES:
            importlib.import_module(f"JhoomMusic.plugins.{module}")
        print("Successfully imported all modules")

        # Start userbot
        if userbot:
            pass

        # Start TgCaller
        await Jhoom.start()
        await Jhoom.decorators()

    except Exception as e:
        print(f"Error during initialization: {e}")
ALL_MODULES = [
    "start",
    "ping",
    "play",
    "auth",
    "lyrics",
    "settings",
    "callback",
    "admins",
    "radio",
    "queue",
    "seek_controls",
    "loop_controls",
    "speed_controls",
    "extras",
    "blacklist_chats",
    "block_users",
    "broadcast",
    "developer",
    "channel_play",
    "global_bans",
    "commands"
]

import importlib
for module in ALL_MODULES:
    importlib.import_module(f"JhoomMusic.plugins.{module}")
print("✅ All plugins imported successfully")


if __name__ == "__main__":
    app.run()
