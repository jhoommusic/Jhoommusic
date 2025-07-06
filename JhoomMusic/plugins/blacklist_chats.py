from pyrogram import filters
from pyrogram.types import Message

from JhoomMusic import app
from JhoomMusic.misc import SUDOERS
from JhoomMusic.utils.database.chats import blacklist_chat, whitelist_chat, is_blacklisted_chat, get_served_chats
from config import BANNED_USERS

@app.on_message(filters.command(["blacklistchat", "blchat"]) & SUDOERS )
async def blacklist_chat_command(client, message: Message):
    """Blacklist a chat from using the bot"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/blacklistchat <chat_id>` - Blacklist chat\n"
            "• `/blacklistchat` (in group) - Blacklist current chat\n\n"
            "**Example:** `/blacklistchat -1001234567890`"
        )
    
    # Get chat ID
    if len(message.command) == 1:
        # Blacklist current chat
        chat_id = message.chat.id
        chat_name = message.chat.title or "Private Chat"
    else:
        try:
            chat_id = int(message.command[1])
            try:
                chat = await app.get_chat(chat_id)
                chat_name = chat.title or chat.first_name or "Unknown"
            except:
                chat_name = "Unknown Chat"
        except ValueError:
            return await message.reply_text("❌ **Invalid chat ID!**")
    
    # Check if already blacklisted
    if await is_blacklisted_chat(chat_id):
        return await message.reply_text("❌ **Chat is already blacklisted!**")
    
    # Blacklist the chat
    await blacklist_chat(chat_id)
    
    await message.reply_text(
        f"🚫 **Chat Blacklisted!**\n\n"
        f"**Chat:** {chat_name}\n"
        f"**ID:** `{chat_id}`\n\n"
        f"**This chat can no longer use the bot.**"
    )

@app.on_message(filters.command(["whitelistchat", "wlchat"]) & SUDOERS )
async def whitelist_chat_command(client, message: Message):
    """Remove chat from blacklist"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/whitelistchat <chat_id>` - Whitelist chat\n"
            "• `/whitelistchat` (in group) - Whitelist current chat\n\n"
            "**Example:** `/whitelistchat -1001234567890`"
        )
    
    # Get chat ID
    if len(message.command) == 1:
        # Whitelist current chat
        chat_id = message.chat.id
        chat_name = message.chat.title or "Private Chat"
    else:
        try:
            chat_id = int(message.command[1])
            try:
                chat = await app.get_chat(chat_id)
                chat_name = chat.title or chat.first_name or "Unknown"
            except:
                chat_name = "Unknown Chat"
        except ValueError:
            return await message.reply_text("❌ **Invalid chat ID!**")
    
    # Check if blacklisted
    if not await is_blacklisted_chat(chat_id):
        return await message.reply_text("❌ **Chat is not blacklisted!**")
    
    # Whitelist the chat
    await whitelist_chat(chat_id)
    
    await message.reply_text(
        f"✅ **Chat Whitelisted!**\n\n"
        f"**Chat:** {chat_name}\n"
        f"**ID:** `{chat_id}`\n\n"
        f"**This chat can now use the bot again.**"
    )

@app.on_message(filters.command(["blacklistedchats", "blchats"]) & SUDOERS )
async def blacklisted_chats_list(client, message: Message):
    """Show list of blacklisted chats"""
    
    mystic = await message.reply_text("📊 **Getting blacklisted chats...**")
    
    try:
        # Get all served chats
        all_chats = await get_served_chats()
        blacklisted_chats = []
        
        for chat_id in all_chats:
            if await is_blacklisted_chat(chat_id):
                blacklisted_chats.append(chat_id)
        
        if not blacklisted_chats:
            return await mystic.edit_text(
                "📭 **No Blacklisted Chats**\n\n"
                "Use `/blacklistchat <chat_id>` to blacklist chats."
            )
        
        blacklist_text = "🚫 **Blacklisted Chats:**\n\n"
        
        for i, chat_id in enumerate(blacklisted_chats[:20], 1):  # Limit to 20
            try:
                chat = await app.get_chat(chat_id)
                chat_name = chat.title or chat.first_name or "Unknown"
                blacklist_text += f"{i}. **{chat_name}** (`{chat_id}`)\n"
            except:
                blacklist_text += f"{i}. **Unknown Chat** (`{chat_id}`)\n"
        
        if len(blacklisted_chats) > 20:
            blacklist_text += f"\n**... and {len(blacklisted_chats) - 20} more chats**"
        
        blacklist_text += f"\n\n**Total:** {len(blacklisted_chats)} chats"
        
        await mystic.edit_text(blacklist_text)
        
    except Exception as e:
        await mystic.edit_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["clearblacklist"]) & SUDOERS )
async def clear_blacklisted_chats(client, message: Message):
    """Clear all blacklisted chats"""
    
    mystic = await message.reply_text("🔄 **Clearing blacklisted chats...**")
    
    try:
        # Get all served chats
        all_chats = await get_served_chats()
        cleared_count = 0
        
        for chat_id in all_chats:
            if await is_blacklisted_chat(chat_id):
                await whitelist_chat(chat_id)
                cleared_count += 1
        
        if cleared_count == 0:
            return await mystic.edit_text("📭 **No blacklisted chats to clear!**")
        
        await mystic.edit_text(
            f"🗑️ **All Blacklisted Chats Cleared!**\n\n"
            f"**Removed:** {cleared_count} chats"
        )
        
    except Exception as e:
        await mystic.edit_text(f"❌ **Error:** {str(e)}")

# Filter to check if chat is blacklisted
@app.on_message(filters.group)
async def check_blacklisted_chats(client, message: Message):
    """Check if chat is blacklisted before processing any command"""
    if await is_blacklisted_chat(message.chat.id):
        await message.reply_text(
            "🚫 **This chat is blacklisted!**\n\n"
            "Contact bot administrators for more information."
        )
        return