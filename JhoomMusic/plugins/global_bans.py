from pyrogram import filters
from pyrogram.types import Message

from JhoomMusic import app
from JhoomMusic.misc import SUDOERS
from JhoomMusic.utils.database.users import add_user, get_user_info
from config import BANNED_USERS, OWNER_ID

# Global banned users list
GLOBAL_BANNED_USERS = []

@app.on_message(filters.command(["gban", "globalban"]) & SUDOERS )
async def global_ban_user(client, message: Message):
    """Globally ban user from all groups"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/gban @username <reason>` - Globally ban user\n"
            "• `/gban user_id <reason>` - Globally ban user by ID\n"
            "• `/gban` (reply to user) `<reason>` - Globally ban replied user\n\n"
            "**Example:** `/gban @spammer Spamming in groups`"
        )
    
    # Get user to ban
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
        reason = " ".join(message.command[1:]) if len(message.command) > 1 else "No reason provided"
    else:
        try:
            if message.command[1].startswith("@"):
                user = await app.get_users(message.command[1])
                user_id = user.id
                user_name = user.first_name
                reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided"
            else:
                user_id = int(message.command[1])
                user = await app.get_users(user_id)
                user_name = user.first_name
                reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided"
        except:
            return await message.reply_text("❌ **User not found!**")
    
    # Check if user is owner or sudo
    if user_id in OWNER_ID:
        return await message.reply_text("❌ **Cannot globally ban bot owner!**")
    
    if user_id in SUDOERS:
        return await message.reply_text("❌ **Cannot globally ban sudo user!**")
    
    # Check if already globally banned
    if any(ban['user_id'] == user_id for ban in GLOBAL_BANNED_USERS):
        return await message.reply_text("❌ **User is already globally banned!**")
    
    # Add to global ban list
    ban_info = {
        "user_id": user_id,
        "user_name": user_name,
        "reason": reason,
        "banned_by": message.from_user.id,
        "banned_by_name": message.from_user.first_name
    }
    
    GLOBAL_BANNED_USERS.append(ban_info)
    
    await message.reply_text(
        f"🌍 **User Globally Banned!**\n\n"
        f"**User:** {user_name}\n"
        f"**ID:** `{user_id}`\n"
        f"**Reason:** {reason}\n"
        f"**Banned by:** {message.from_user.first_name}\n\n"
        f"**{user_name}** is now banned from all groups using this bot."
    )

@app.on_message(filters.command(["ungban", "unglobalban"]) & SUDOERS )
async def global_unban_user(client, message: Message):
    """Remove user from global ban list"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/ungban @username` - Remove global ban\n"
            "• `/ungban user_id` - Remove global ban by ID\n"
            "• `/ungban` (reply to user) - Remove global ban from replied user"
        )
    
    # Get user to unban
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    else:
        try:
            if message.command[1].startswith("@"):
                user = await app.get_users(message.command[1])
                user_id = user.id
                user_name = user.first_name
            else:
                user_id = int(message.command[1])
                user = await app.get_users(user_id)
                user_name = user.first_name
        except:
            return await message.reply_text("❌ **User not found!**")
    
    # Find and remove from global ban list
    ban_info = None
    for ban in GLOBAL_BANNED_USERS:
        if ban['user_id'] == user_id:
            ban_info = ban
            GLOBAL_BANNED_USERS.remove(ban)
            break
    
    if not ban_info:
        return await message.reply_text("❌ **User is not globally banned!**")
    
    await message.reply_text(
        f"✅ **Global Ban Removed!**\n\n"
        f"**User:** {user_name}\n"
        f"**ID:** `{user_id}`\n"
        f"**Previous Reason:** {ban_info['reason']}\n"
        f"**Unbanned by:** {message.from_user.first_name}\n\n"
        f"**{user_name}** can now use the bot in all groups again."
    )

@app.on_message(filters.command(["gbannedusers", "gbanlist"]) & SUDOERS )
async def global_banned_users_list(client, message: Message):
    """Show list of globally banned users"""
    
    if not GLOBAL_BANNED_USERS:
        return await message.reply_text(
            "📭 **No Globally Banned Users**\n\n"
            "Use `/gban @username <reason>` to globally ban users."
        )
    
    gban_text = "🌍 **Globally Banned Users:**\n\n"
    
    for i, ban in enumerate(GLOBAL_BANNED_USERS[:20], 1):  # Limit to 20
        gban_text += f"{i}. **{ban['user_name']}** (`{ban['user_id']}`)\n"
        gban_text += f"   **Reason:** {ban['reason']}\n"
        gban_text += f"   **Banned by:** {ban['banned_by_name']}\n\n"
    
    if len(GLOBAL_BANNED_USERS) > 20:
        gban_text += f"**... and {len(GLOBAL_BANNED_USERS) - 20} more users**\n\n"
    
    gban_text += f"**Total:** {len(GLOBAL_BANNED_USERS)} users"
    
    await message.reply_text(gban_text)

@app.on_message(filters.command(["cleargbans"]) & SUDOERS )
async def clear_global_bans(client, message: Message):
    """Clear all global bans"""
    
    if not GLOBAL_BANNED_USERS:
        return await message.reply_text("📭 **No globally banned users to clear!**")
    
    count = len(GLOBAL_BANNED_USERS)
    GLOBAL_BANNED_USERS.clear()
    
    await message.reply_text(
        f"🗑️ **All Global Bans Cleared!**\n\n"
        f"**Removed:** {count} users"
    )

@app.on_message(filters.command(["gbaninfo"]) & SUDOERS )
async def global_ban_info(client, message: Message):
    """Get information about a globally banned user"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/gbaninfo @username` - Get ban info\n"
            "• `/gbaninfo user_id` - Get ban info by ID\n"
            "• `/gbaninfo` (reply to user) - Get ban info for replied user"
        )
    
    # Get user to check
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    else:
        try:
            if message.command[1].startswith("@"):
                user = await app.get_users(message.command[1])
                user_id = user.id
                user_name = user.first_name
            else:
                user_id = int(message.command[1])
                user = await app.get_users(user_id)
                user_name = user.first_name
        except:
            return await message.reply_text("❌ **User not found!**")
    
    # Find ban info
    ban_info = None
    for ban in GLOBAL_BANNED_USERS:
        if ban['user_id'] == user_id:
            ban_info = ban
            break
    
    if not ban_info:
        return await message.reply_text(
            f"✅ **{user_name}** is not globally banned."
        )
    
    await message.reply_text(
        f"🌍 **Global Ban Information**\n\n"
        f"**User:** {ban_info['user_name']}\n"
        f"**ID:** `{ban_info['user_id']}`\n"
        f"**Reason:** {ban_info['reason']}\n"
        f"**Banned by:** {ban_info['banned_by_name']}\n"
        f"**Status:** Globally Banned"
    )

# Filter to check if user is globally banned
def is_globally_banned(user_id: int) -> bool:
    """Check if user is globally banned"""
    return any(ban['user_id'] == user_id for ban in GLOBAL_BANNED_USERS)

# Check global bans for all messages
@app.on_message(filters.all & filters.group)
async def check_global_bans(client, message: Message):
    """Check if user is globally banned before processing any command"""
    if message.from_user and is_globally_banned(message.from_user.id):
        # Find ban info
        ban_info = None
        for ban in GLOBAL_BANNED_USERS:
            if ban['user_id'] == message.from_user.id:
                ban_info = ban
                break
        
        if ban_info:
            await message.reply_text(
                f"🌍 **You are globally banned!**\n\n"
                f"**Reason:** {ban_info['reason']}\n"
                f"**Banned by:** {ban_info['banned_by_name']}\n\n"
                f"Contact bot administrators if you think this is a mistake."
            )
        return