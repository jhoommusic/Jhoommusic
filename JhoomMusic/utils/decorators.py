from functools import wraps
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

from JhoomMusic import app
from JhoomMusic.utils.database import get_authuser_names, get_authuser
from config import OWNER_ID, SUDO_USERS


def AdminRightsCheck(f):
    @wraps(f)
    async def decorated(client, message: Message, *args, **kwargs):
        if message.from_user.id in OWNER_ID:
            return await f(client, message, *args, **kwargs)
        
        if message.from_user.id in SUDO_USERS:
            return await f(client, message, *args, **kwargs)
        
        try:
            user = await app.get_chat_member(message.chat.id, message.from_user.id)
            if user.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await f(client, message, *args, **kwargs)
        except:
            pass
        
        # Check if user is in auth list
        if await get_authuser(message.chat.id, message.from_user.id):
            return await f(client, message, *args, **kwargs)
        
        return await message.reply_text(
            "❌ **Access Denied!**\n\nYou need to be an admin or authorized user to use this command."
        )
    
    return decorated


def language(f):
    @wraps(f)
    async def decorated(client, message: Message, *args, **kwargs):
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("en")
        return await f(client, message, language, *args, **kwargs)
    
    return decorated