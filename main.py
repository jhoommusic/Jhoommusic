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
            if userbot:
    if userbot:
    if userbot:
        
        # Start TgCaller
        await Jhoom.start()
        await Jhoom.decorators()
        
        print("🎵 JhoomMusic Bot Started Successfully!")
        
        # Keep the bot running
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"Error starting bot: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(init())