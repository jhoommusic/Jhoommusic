from pyrogram import filters
from pyrogram.types import Message

from JhoomMusic import app
from JhoomMusic.utils.decorators import AdminRightsCheck
from JhoomMusic.utils.database.database import save_authuser, delete_authuser, _get_authuser_names, is_nonadmin
from config import BANNED_USERS

@app.on_message(filters.command(["auth"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def auth_user(client, message: Message, _, chat_id):
    """Authorize user to use music commands"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/auth @username` - Authorize user\n"
            "• `/auth` (reply to user) - Authorize replied user"
        )
    
    # Get user to authorize
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    else:
        try:
            user = await app.get_users(message.command[1])
            user_id = user.id
            user_name = user.first_name
        except:
            return await message.reply_text("❌ **User not found!**")
    
    # Check if already authorized
    if not await is_nonadmin(chat_id, user_id):
        return await message.reply_text("✅ **User is already authorized!**")
    
    # Authorize user
    await save_authuser(chat_id, user_id, user_name)
    
    await message.reply_text(
        f"✅ **User Authorized!**\n\n"
        f"**User:** {user_name}\n"
        f"**ID:** `{user_id}`\n\n"
        f"**{user_name}** can now use music commands in this group."
    )

@app.on_message(filters.command(["unauth"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def unauth_user(client, message: Message, _, chat_id):
    """Remove user authorization"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/unauth @username` - Remove authorization\n"
            "• `/unauth` (reply to user) - Remove replied user's authorization"
        )
    
    # Get user to unauthorize
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    else:
        try:
            user = await app.get_users(message.command[1])
            user_id = user.id
            user_name = user.first_name
        except:
            return await message.reply_text("❌ **User not found!**")
    
    # Check if user is authorized
    if await is_nonadmin(chat_id, user_id):
        return await message.reply_text("❌ **User is not authorized!**")
    
    # Remove authorization
    await delete_authuser(chat_id, user_id)
    
    await message.reply_text(
        f"❌ **Authorization Removed!**\n\n"
        f"**User:** {user_name}\n"
        f"**ID:** `{user_id}`\n\n"
        f"**{user_name}** can no longer use music commands in this group."
    )

@app.on_message(filters.command(["authusers", "authlist"]) & filters.group & ~BANNED_USERS)
async def auth_users_list(client, message: Message):
    """Show list of authorized users"""
    
    chat_id = message.chat.id
    auth_users = await _get_authuser_names(chat_id)
    
    if not auth_users:
        return await message.reply_text(
            "📭 **No Authorized Users**\n\n"
            "Use `/auth @username` to authorize users."
        )
    
    auth_text = "👥 **Authorized Users:**\n\n"
    
    for i, user in enumerate(auth_users, 1):
        auth_text += f"{i}. **{user['user_name']}** (`{user['user_id']}`)\n"
    
    auth_text += f"\n**Total:** {len(auth_users)} users"
    
    await message.reply_text(auth_text)

@app.on_message(filters.command(["clearauth"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def clear_auth_users(client, message: Message, _, chat_id):
    """Clear all authorized users"""
    
    auth_users = await _get_authuser_names(chat_id)
    
    if not auth_users:
        return await message.reply_text("📭 **No authorized users to clear!**")
    
    # Clear all authorized users
    for user in auth_users:
        await delete_authuser(chat_id, user['user_id'])
    
    await message.reply_text(
        f"🗑️ **All Authorized Users Cleared!**\n\n"
        f"**Removed:** {len(auth_users)} users"
    )