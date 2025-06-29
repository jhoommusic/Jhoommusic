import sys
import heroku3
from pyrogram import filters

import config
from .logging import LOGGER

SUDOERS = filters.user()
BANNED_USERS = filters.user()


def sudo():
    global SUDOERS
    if config.OWNER_ID:
        for user_id in config.OWNER_ID:
            SUDOERS.add(user_id)
    if config.SUDO_USERS:
        for user_id in config.SUDO_USERS:
            SUDOERS.add(user_id)


def dbb():
    global db
    db = {}
    LOGGER(__name__).info("Local Database Initialized")


def heroku():
    global herokuapp
    if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
        try:
            Heroku = heroku3.from_key(config.HEROKU_API_KEY)
            herokuapp = Heroku.apps()[config.HEROKU_APP_NAME]
            LOGGER(__name__).info("Heroku App Configured")
        except Exception as e:
            LOGGER(__name__).warning(f"Heroku App not found: {e}")
            herokuapp = None
    else:
        herokuapp = None


def banned_users():
    global BANNED_USERS
    # Initialize banned users filter
    for user_id in config.BANNED_USERS:
        BANNED_USERS.add(user_id)


async def is_banned_user(user_id: int) -> bool:
    """Check if user is banned"""
    return user_id in config.BANNED_USERS


async def ban_user(user_id: int):
    """Ban a user"""
    if user_id not in config.BANNED_USERS:
        config.BANNED_USERS.append(user_id)
        BANNED_USERS.add(user_id)


async def unban_user(user_id: int):
    """Unban a user"""
    if user_id in config.BANNED_USERS:
        config.BANNED_USERS.remove(user_id)
        BANNED_USERS.remove(user_id)