from functools import wraps
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

from config import OWNER_ID, SUDO_USERS

def AdminRightsCheck(f):
    from JhoomMusic import app  # lazy import
    """Decorator to check admin rights"""
    @wraps(f)
    async def decorated(client, message: Message, *args, **kwargs):
        # Check if user is owner
        if message.from_user.id in OWNER_ID:
            return await f(client, message, *args, **kwargs)
        
        # Check if user is sudo user
        if message.from_user.id in SUDO_USERS:
            return await f(client, message, *args, **kwargs)
        
        # Check if user is admin in the chat
        try:
            user = await app.get_chat_member(message.chat.id, message.from_user.id)
            if user.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await f(client, message, *args, **kwargs)
        except:
            pass
        
        # User doesn't have required permissions
        return await message.reply_text(
            "❌ **Access Denied!**\n\n"
            "You need to be an admin to use this command."
        )
    
    return decorated

def language(f):
    """Decorator for language support"""
    @wraps(f)
    async def decorated(client, message: Message, *args, **kwargs):
        try:
            # For now, use English as default
            language = "en"
        except:
            language = "en"
        return await f(client, message, language, *args, **kwargs)
    
    return decorated

def ActualAdminCB(f):
    """Decorator for callback query admin check"""
    @wraps(f)
    async def decorated(client, callback_query, *args, **kwargs):
        # Check if user is owner
        if callback_query.from_user.id in OWNER_ID:
            return await f(client, callback_query, *args, **kwargs)
        
        # Check if user is sudo user
        if callback_query.from_user.id in SUDO_USERS:
            return await f(client, callback_query, *args, **kwargs)
        
        # Check if user is admin in the chat
        try:
            user = await app.get_chat_member(
                callback_query.message.chat.id, 
                callback_query.from_user.id
            )
            if user.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await f(client, callback_query, *args, **kwargs)
        except:
            pass
        
        # User doesn't have required permissions
        return await callback_query.answer(
            "❌ You need to be an admin to use this!",
            show_alert=True
        )
    
    return decorated

def check_blacklist(f):
    """Decorator to check if user/chat is blacklisted"""
    @wraps(f)
    async def decorated(client, message: Message, *args, **kwargs):
        # Add blacklist checking logic here
        # For now, just proceed
        return await f(client, message, *args, **kwargs)
    
    return decorated