from pyrogram import filters
from pyrogram.types import Message

from JhoomMusic import app
from JhoomMusic.misc import SUDOERS
from JhoomMusic.utils.database.users import add_user, get_user_info
from config import BANNED_USERS, OWNER_ID

# Global blocked users list
BLOCKED_USERS = []

@app.on_message(filters.command(["block"]) & SUDOERS & ~BANNED_USERS)
async def block_user(client, message: Message):
    """Block user from using the bot"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/block @username` - Block user\n"
            "• `/block user_id` - Block user by ID\n"
            "• `/block` (reply to user) - Block replied user"
        )
    
    # Get user to block
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
    
    # Check if user is owner or sudo
    if user_id in OWNER_ID:
        return await message.reply_text("❌ **Cannot block bot owner!**")
    
    # Block user
    if user_id not in BLOCKED_USERS:
        BLOCKED_USERS.append(user_id)
        
        await message.reply_text(
            f"🚫 **User Blocked!**\n\n"
            f"**User:** {user_name}\n"
            f"**ID:** `{user_id}`\n\n"
            f"**{user_name}** can no longer use the bot."
        )
    else:
        await message.reply_text("❌ **User is already blocked!**")

@app.on_message(filters.command(["unblock"]) & SUDOERS & ~BANNED_USERS)
async def unblock_user(client, message: Message):
    """Unblock user from using the bot"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/unblock @username` - Unblock user\n"
            "• `/unblock user_id` - Unblock user by ID\n"
            "• `/unblock` (reply to user) - Unblock replied user"
        )
    
    # Get user to unblock
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
    
    # Unblock user
    if user_id in BLOCKED_USERS:
        BLOCKED_USERS.remove(user_id)
        
        await message.reply_text(
            f"✅ **User Unblocked!**\n\n"
            f"**User:** {user_name}\n"
            f"**ID:** `{user_id}`\n\n"
            f"**{user_name}** can now use the bot again."
        )
    else:
        await message.reply_text("❌ **User is not blocked!**")

@app.on_message(filters.command(["blockedusers", "blocklist"]) & SUDOERS & ~BANNED_USERS)
async def blocked_users_list(client, message: Message):
    """Show list of blocked users"""
    
    if not BLOCKED_USERS:
        return await message.reply_text(
            "📭 **No Blocked Users**\n\n"
            "Use `/block @username` to block users."
        )
    
    blocked_text = "🚫 **Blocked Users:**\n\n"
    
    for i, user_id in enumerate(BLOCKED_USERS, 1):
        try:
            user = await app.get_users(user_id)
            blocked_text += f"{i}. **{user.first_name}** (`{user_id}`)\n"
        except:
            blocked_text += f"{i}. **Unknown User** (`{user_id}`)\n"
    
    blocked_text += f"\n**Total:** {len(BLOCKED_USERS)} users"
    
    await message.reply_text(blocked_text)

@app.on_message(filters.command(["clearblocked"]) & SUDOERS & ~BANNED_USERS)
async def clear_blocked_users(client, message: Message):
    """Clear all blocked users"""
    
    if not BLOCKED_USERS:
        return await message.reply_text("📭 **No blocked users to clear!**")
    
    count = len(BLOCKED_USERS)
    BLOCKED_USERS.clear()
    
    await message.reply_text(
        f"🗑️ **All Blocked Users Cleared!**\n\n"
        f"**Removed:** {count} users"
    )

# Filter to check if user is blocked
def is_blocked_user(user_id: int) -> bool:
    """Check if user is blocked"""
    return user_id in BLOCKED_USERS

# Add blocked users filter to existing BANNED_USERS
@app.on_message(filters.all & filters.private)
async def check_blocked_users(client, message: Message):
    """Check if user is blocked before processing any command"""
    if message.from_user and is_blocked_user(message.from_user.id):
        await message.reply_text(
            "🚫 **You are blocked from using this bot!**\n\n"
            "Contact bot administrators if you think this is a mistake."
        )
        return