#!/usr/bin/env python3
"""
JhoomMusic Bot - Clean Entry Point
"""

import asyncio
import sys
import importlib
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from JhoomMusic.logging import LOGGER
from JhoomMusic import app, userbot
from JhoomMusic.core.call import Jhoom
from JhoomMusic.core.dir import dirr
from JhoomMusic.misc import sudo, dbb, heroku, banned_users
from JhoomMusic.plugins import ALL_MODULES
import config


async def main():
    LOGGER(__name__).info("🎵 Starting JhoomMusic Bot...")

    # 1. Create required folders
    dirr()

    # 2. Initialize helpers
    dbb()
    heroku()
    sudo()
    banned_users()

    # 3. Start main bot
    await app.start()
    me = await app.get_me()
    app.username = me.username
    app.id = me.id
    app.name = me.first_name
    LOGGER(__name__).info(f"✅ Bot started as @{me.username}")

    # 4. Load all plugins
    loaded = 0
    for module in ALL_MODULES:
        try:
            importlib.import_module(f"JhoomMusic.plugins.{module}")
            loaded += 1
        except Exception as e:
            LOGGER(__name__).error(f"Failed to load plugin {module}: {e}")

    LOGGER(__name__).info(f"✅ Loaded {loaded}/{len(ALL_MODULES)} plugins")

    # 5. Start userbot (if available)
    if userbot:
        try:
            await userbot.start()
            LOGGER(__name__).info("✅ Userbot started")
        except Exception as e:
            LOGGER(__name__).error(f"Userbot failed to start: {e}")
    else:
        LOGGER(__name__).warning("⚠️ Userbot is disabled")

    # 6. Start TgCaller
    try:
        await Jhoom.start()
        await Jhoom.decorators()
        LOGGER(__name__).info("✅ TgCaller started")
    except Exception as e:
        LOGGER(__name__).error(f"TgCaller failed: {e}")

    # 7. Notify log group
    if config.LOG_GROUP_ID:
        try:
            await app.send_message(
                config.LOG_GROUP_ID,
                f"🎵 **JhoomMusic Started**\n\n"
                f"• Bot: @{app.username}\n"
                f"• Userbot: {'Active' if userbot else 'Disabled'}\n"
                f"• Plugins: {loaded}\n"
                f"• Status: Ready"
            )
        except Exception as e:
            LOGGER(__name__).warning(f"Could not send startup message: {e}")

    LOGGER(__name__).info("🎵 JhoomMusic is now running!")

    # Keep alive
    await asyncio.Event().wait()


async def stop():
    """Graceful shutdown"""
    try:
        await Jhoom.stop()
    except Exception:
        pass
    if userbot:
        try:
            await userbot.stop()
        except Exception:
            pass
    try:
        await app.stop()
    except Exception:
        pass
    LOGGER(__name__).info("Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER(__name__).info("Stopped by user")
        try:
            asyncio.run(stop())
        except Exception:
            pass
    except Exception as e:
        LOGGER(__name__).error(f"Fatal error: {e}")
        sys.exit(1)
