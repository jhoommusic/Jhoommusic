from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from JhoomMusic import app
from JhoomMusic.utils.decorators import AdminRightsCheck
from JhoomMusic.utils.formatters import seconds_to_min
from config import BANNED_USERS

@app.on_message(filters.command(["seek"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def seek_command(client, message: Message, _, chat_id):
    """Seek to specific position in track"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/seek <time>`\n\n"
            "**Time Formats:**\n"
            "• `/seek 1:30` - Seek to 1 minute 30 seconds\n"
            "• `/seek 90` - Seek to 90 seconds\n"
            "• `/seek 2:15` - Seek to 2 minutes 15 seconds\n\n"
            "**Examples:**\n"
            "• `/seek 45` - Seek to 45 seconds\n"
            "• `/seek 3:20` - Seek to 3 minutes 20 seconds"
        )
    
    time_str = message.command[1]
    
    try:
        # Parse time string
        if ":" in time_str:
            # Format: MM:SS or HH:MM:SS
            parts = time_str.split(":")
            if len(parts) == 2:  # MM:SS
                minutes, seconds = map(int, parts)
                total_seconds = minutes * 60 + seconds
            elif len(parts) == 3:  # HH:MM:SS
                hours, minutes, seconds = map(int, parts)
                total_seconds = hours * 3600 + minutes * 60 + seconds
            else:
                raise ValueError("Invalid time format")
        else:
            # Format: seconds only
            total_seconds = int(time_str)
        
        if total_seconds < 0:
            return await message.reply_text("❌ **Time cannot be negative!**")
        
        # For now, this is a placeholder as actual seeking requires PyTgCalls implementation
        await message.reply_text(
            f"⏩ **Seeking to {seconds_to_min(total_seconds)}**\n\n"
            f"**Position:** {total_seconds} seconds\n\n"
            f"⚠️ **Note:** Seek functionality is under development.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("⏪ -30s", callback_data=f"seek_back_30_{chat_id}"),
                    InlineKeyboardButton("⏩ +30s", callback_data=f"seek_forward_30_{chat_id}")
                ],
                [
                    InlineKeyboardButton("⏪ -10s", callback_data=f"seek_back_10_{chat_id}"),
                    InlineKeyboardButton("⏩ +10s", callback_data=f"seek_forward_10_{chat_id}")
                ]
            ])
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid time format!**\n\n"
            "**Valid formats:**\n"
            "• `45` (seconds)\n"
            "• `1:30` (minutes:seconds)\n"
            "• `1:05:30` (hours:minutes:seconds)"
        )

@app.on_message(filters.command(["seekback", "rewind"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def seekback_command(client, message: Message, _, chat_id):
    """Seek backwards in track"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/seekback <time>`\n\n"
            "**Examples:**\n"
            "• `/seekback 30` - Go back 30 seconds\n"
            "• `/seekback 1:00` - Go back 1 minute"
        )
    
    time_str = message.command[1]
    
    try:
        # Parse time string
        if ":" in time_str:
            parts = time_str.split(":")
            if len(parts) == 2:  # MM:SS
                minutes, seconds = map(int, parts)
                total_seconds = minutes * 60 + seconds
            else:
                raise ValueError("Invalid time format")
        else:
            total_seconds = int(time_str)
        
        if total_seconds < 0:
            return await message.reply_text("❌ **Time cannot be negative!**")
        
        await message.reply_text(
            f"⏪ **Seeking back {seconds_to_min(total_seconds)}**\n\n"
            f"**Rewind:** {total_seconds} seconds\n\n"
            f"⚠️ **Note:** Seek functionality is under development."
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid time format!**\n\n"
            "Use format like: `30` or `1:30`"
        )

@app.on_message(filters.command(["seekforward", "fastforward"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def seekforward_command(client, message: Message, _, chat_id):
    """Seek forward in track"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/seekforward <time>`\n\n"
            "**Examples:**\n"
            "• `/seekforward 30` - Go forward 30 seconds\n"
            "• `/seekforward 1:00` - Go forward 1 minute"
        )
    
    time_str = message.command[1]
    
    try:
        # Parse time string
        if ":" in time_str:
            parts = time_str.split(":")
            if len(parts) == 2:  # MM:SS
                minutes, seconds = map(int, parts)
                total_seconds = minutes * 60 + seconds
            else:
                raise ValueError("Invalid time format")
        else:
            total_seconds = int(time_str)
        
        if total_seconds < 0:
            return await message.reply_text("❌ **Time cannot be negative!**")
        
        await message.reply_text(
            f"⏩ **Seeking forward {seconds_to_min(total_seconds)}**\n\n"
            f"**Fast forward:** {total_seconds} seconds\n\n"
            f"⚠️ **Note:** Seek functionality is under development."
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid time format!**\n\n"
            "Use format like: `30` or `1:30`"
        )

# Callback handlers for seek buttons
@app.on_callback_query(filters.regex(r"seek_back_(\d+)_(.*)"))
async def seek_back_callback(client, callback_query):
    """Handle seek back button"""
    seconds = int(callback_query.data.split("_")[2])
    chat_id = int(callback_query.data.split("_")[3])
    
    # Placeholder implementation
    await callback_query.answer(f"⏪ Seeking back {seconds} seconds", show_alert=False)
    
    # In actual implementation, this would call PyTgCalls seek function
    # await Jhoom.seek_stream(chat_id, -seconds)

@app.on_callback_query(filters.regex(r"seek_forward_(\d+)_(.*)"))
async def seek_forward_callback(client, callback_query):
    """Handle seek forward button"""
    seconds = int(callback_query.data.split("_")[2])
    chat_id = int(callback_query.data.split("_")[3])
    
    # Placeholder implementation
    await callback_query.answer(f"⏩ Seeking forward {seconds} seconds", show_alert=False)
    
    # In actual implementation, this would call PyTgCalls seek function
    # await Jhoom.seek_stream(chat_id, seconds)

@app.on_message(filters.command(["position", "pos"]) & filters.group & ~BANNED_USERS)
async def current_position(client, message: Message):
    """Show current playback position"""
    
    chat_id = message.chat.id
    
    # Placeholder - in actual implementation, get from PyTgCalls
    current_pos = 0  # This would be fetched from the actual player
    total_duration = 0  # This would be the track duration
    
    if current_pos == 0 and total_duration == 0:
        await message.reply_text(
            "❌ **No track currently playing**\n\n"
            "Use `/play <song>` to start playing music."
        )
    else:
        progress_bar = create_progress_bar(current_pos, total_duration)
        
        await message.reply_text(
            f"🎵 **Current Position**\n\n"
            f"**Time:** {seconds_to_min(current_pos)} / {seconds_to_min(total_duration)}\n"
            f"**Progress:** {progress_bar}\n\n"
            f"⚠️ **Note:** Position tracking is under development.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("⏪ -30s", callback_data=f"seek_back_30_{chat_id}"),
                    InlineKeyboardButton("⏩ +30s", callback_data=f"seek_forward_30_{chat_id}")
                ]
            ])
        )

def create_progress_bar(current: int, total: int, length: int = 20) -> str:
    """Create a visual progress bar"""
    if total == 0:
        return "▱" * length
    
    progress = min(current / total, 1.0)
    filled = int(progress * length)
    
    bar = "▰" * filled + "▱" * (length - filled)
    percentage = int(progress * 100)
    
    return f"{bar} {percentage}%"

@app.on_message(filters.command(["seekhelp"]) & ~BANNED_USERS)
async def seek_help(client, message: Message):
    """Show seek commands help"""
    
    help_text = """
🎯 **SEEK COMMANDS HELP**

**Basic Seek Commands:**
• `/seek <time>` - Seek to specific position
• `/seekback <time>` - Seek backwards
• `/seekforward <time>` - Seek forwards
• `/position` - Show current position

**Time Formats:**
• `30` - 30 seconds
• `1:30` - 1 minute 30 seconds
• `2:15:45` - 2 hours 15 minutes 45 seconds

**Quick Seek:**
• `/seek 0` - Go to beginning
• `/seekback 10` - Go back 10 seconds
• `/seekforward 30` - Go forward 30 seconds

**Examples:**
• `/seek 1:45` - Jump to 1 minute 45 seconds
• `/seekback 30` - Go back 30 seconds
• `/position` - Show current playback position

**Note:** Seek functionality requires active music playback.
"""
    
    await message.reply_text(help_text)