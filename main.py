#!/usr/bin/env python3
"""
JhoomMusic Bot - Main Entry Point
Advanced Telegram Music Bot with Auto-Update System
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

# Configure logging before importing other modules
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

# Suppress noisy loggers
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

async def main():
    """Main function to start the bot"""
    try:
        LOGGER.info("🎵 Starting JhoomMusic Bot...")
        
        # Import after logging setup
        from JhoomMusic import app, userbot
        from JhoomMusic.core.call import Jhoom
        from JhoomMusic.misc import sudo
        from JhoomMusic.plugins import ALL_MODULES
        import importlib
        
        # Initialize sudo users
        await sudo()
        LOGGER.info("✅ Sudo users initialized")
        
        # Start the main bot
        await app.start()
        LOGGER.info("✅ Main bot started")
        
        # Import all plugins
        imported_modules = 0
        for module in ALL_MODULES:
            try:
                importlib.import_module(f"JhoomMusic.plugins.{module}")
                imported_modules += 1
            except Exception as e:
                LOGGER.error(f"❌ Failed to import {module}: {e}")
        
        LOGGER.info(f"✅ Successfully imported {imported_modules}/{len(ALL_MODULES)} modules")
        
        # Start userbot if available
        if userbot:
            try:
                await userbot.start()
                LOGGER.info("✅ Userbot started")
            except Exception as e:
                LOGGER.error(f"❌ Failed to start userbot: {e}")
        else:
            LOGGER.warning("⚠️ Userbot not available")
        
        # Start call client
        try:
            await Jhoom.start()
            await Jhoom.decorators()
            LOGGER.info("✅ Call client started")
        except Exception as e:
            LOGGER.error(f"❌ Failed to start call client: {e}")
        
        LOGGER.info("🎵 JhoomMusic Bot Started Successfully!")
        LOGGER.info("✅ Bot is ready to receive commands")
        
        # Send startup message to log group
        try:
            import config
            if config.LOG_GROUP_ID:
                await app.send_message(
                    config.LOG_GROUP_ID,
                    "🎵 **JhoomMusic Bot Started Successfully!**\n\n"
                    f"✅ **Bot:** @{app.username}\n"
                    f"✅ **Userbot:** {'Connected' if userbot else 'Disabled'}\n"
                    f"✅ **Plugins:** {imported_modules} loaded\n"
                    f"✅ **Call Client:** {Jhoom.client if Jhoom.client else 'None'}\n\n"
                    "**Bot is ready to receive commands!**"
                )
        except Exception as e:
            LOGGER.error(f"Failed to send startup message: {e}")
        
        # Keep the bot running
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        LOGGER.info("🛑 Bot stopped by user")
    except Exception as e:
        LOGGER.error(f"❌ Error starting bot: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        try:
            if 'Jhoom' in locals():
                await Jhoom.stop()
            if 'userbot' in locals() and userbot:
                await userbot.stop()
            if 'app' in locals():
                await app.stop()
            LOGGER.info("✅ Bot stopped gracefully")
        except Exception as e:
            LOGGER.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
