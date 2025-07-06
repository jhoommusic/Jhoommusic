from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from JhoomMusic import app
from JhoomMusic.utils.decorators import AdminRightsCheck
from config import BANNED_USERS

# Store speed settings for each chat
SPEED_SETTINGS = {}

@app.on_message(filters.command(["speed"]) & filters.group )
@AdminRightsCheck
async def speed_command(client, message: Message, _, chat_id):
    """Adjust playback speed in group"""
    
    if len(message.command) == 1:
        # Show current speed and options
        current_speed = SPEED_SETTINGS.get(chat_id, 1.0)
        
        await message.reply_text(
            f"⚡ **Playback Speed Control**\n\n"
            f"**Current Speed:** {current_speed}x\n\n"
            f"**Usage:** `/speed <rate>`\n\n"
            f"**Examples:**\n"
            f"• `/speed 1.5` - 1.5x speed (faster)\n"
            f"• `/speed 0.75` - 0.75x speed (slower)\n"
            f"• `/speed 1` - Normal speed\n"
            f"• `/speed 2` - 2x speed (very fast)",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("0.5x", callback_data=f"speed_0.5_{chat_id}"),
                    InlineKeyboardButton("0.75x", callback_data=f"speed_0.75_{chat_id}"),
                    InlineKeyboardButton("1x", callback_data=f"speed_1_{chat_id}")
                ],
                [
                    InlineKeyboardButton("1.25x", callback_data=f"speed_1.25_{chat_id}"),
                    InlineKeyboardButton("1.5x", callback_data=f"speed_1.5_{chat_id}"),
                    InlineKeyboardButton("2x", callback_data=f"speed_2_{chat_id}")
                ]
            ])
        )
        return
    
    try:
        speed = float(message.command[1])
        
        # Validate speed range
        if speed < 0.25 or speed > 3.0:
            return await message.reply_text(
                "❌ **Invalid speed range!**\n\n"
                "**Allowed range:** 0.25x to 3.0x\n"
                "**Examples:** 0.5, 1.0, 1.5, 2.0"
            )
        
        # Set speed
        SPEED_SETTINGS[chat_id] = speed
        
        # Speed descriptions
        if speed < 0.75:
            description = "🐌 Very Slow"
        elif speed < 1.0:
            description = "🚶 Slow"
        elif speed == 1.0:
            description = "🎵 Normal"
        elif speed <= 1.5:
            description = "🏃 Fast"
        else:
            description = "🚀 Very Fast"
        
        await message.reply_text(
            f"⚡ **Speed Set to {speed}x**\n\n"
            f"**Mode:** {description}\n\n"
            f"⚠️ **Note:** Speed control is under development.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔄 Reset to 1x", callback_data=f"speed_1_{chat_id}")
                ]
            ])
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid speed value!**\n\n"
            "**Usage:** `/speed <number>`\n"
            "**Examples:** `/speed 1.5` or `/speed 0.75`"
        )

@app.on_message(filters.command(["cspeed", "channelspeed"]) & filters.group )
@AdminRightsCheck
async def channel_speed_command(client, message: Message, _, chat_id):
    """Adjust playback speed in connected channel"""
    
    # Check if channel is connected (from channel_play.py)
    from JhoomMusic.plugins.channel_play import CHANNEL_CONNECTIONS
    
    if chat_id not in CHANNEL_CONNECTIONS:
        return await message.reply_text(
            "❌ **No channel connected!**\n\n"
            "Use `/channelplay @channel` to connect a channel first."
        )
    
    if len(message.command) == 1:
        # Show current speed for channel
        channel_info = CHANNEL_CONNECTIONS[chat_id]
        channel_id = channel_info["channel_id"]
        channel_name = channel_info["channel_name"]
        current_speed = SPEED_SETTINGS.get(f"channel_{channel_id}", 1.0)
        
        await message.reply_text(
            f"⚡ **Channel Speed Control**\n\n"
            f"**Channel:** {channel_name}\n"
            f"**Current Speed:** {current_speed}x\n\n"
            f"**Usage:** `/cspeed <rate>`",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("0.5x", callback_data=f"cspeed_0.5_{channel_id}"),
                    InlineKeyboardButton("1x", callback_data=f"cspeed_1_{channel_id}"),
                    InlineKeyboardButton("1.5x", callback_data=f"cspeed_1.5_{channel_id}")
                ],
                [
                    InlineKeyboardButton("2x", callback_data=f"cspeed_2_{channel_id}")
                ]
            ])
        )
        return
    
    try:
        speed = float(message.command[1])
        
        if speed < 0.25 or speed > 3.0:
            return await message.reply_text(
                "❌ **Invalid speed range!**\n\n"
                "**Allowed range:** 0.25x to 3.0x"
            )
        
        channel_info = CHANNEL_CONNECTIONS[chat_id]
        channel_id = channel_info["channel_id"]
        channel_name = channel_info["channel_name"]
        
        # Set channel speed
        SPEED_SETTINGS[f"channel_{channel_id}"] = speed
        
        await message.reply_text(
            f"⚡ **Channel Speed Set to {speed}x**\n\n"
            f"**Channel:** {channel_name}\n\n"
            f"⚠️ **Note:** Channel speed control is under development."
        )
        
    except ValueError:
        await message.reply_text("❌ **Invalid speed value!**")

# Callback handlers for speed buttons
@app.on_callback_query(filters.regex(r"speed_(.+)_(.*)"))
async def speed_callback(client, callback_query):
    """Handle speed button callbacks"""
    speed_str = callback_query.data.split("_")[1]
    chat_id = int(callback_query.data.split("_")[2])
    
    try:
        speed = float(speed_str)
        SPEED_SETTINGS[chat_id] = speed
        
        # Speed descriptions
        if speed < 0.75:
            description = "🐌 Very Slow"
        elif speed < 1.0:
            description = "🚶 Slow"
        elif speed == 1.0:
            description = "🎵 Normal"
        elif speed <= 1.5:
            description = "🏃 Fast"
        else:
            description = "🚀 Very Fast"
        
        await callback_query.answer(f"⚡ Speed set to {speed}x", show_alert=False)
        await callback_query.message.edit_text(
            f"⚡ **Speed Set to {speed}x**\n\n"
            f"**Mode:** {description}\n\n"
            f"⚠️ **Note:** Speed control is under development."
        )
        
    except ValueError:
        await callback_query.answer("❌ Invalid speed value", show_alert=True)

@app.on_callback_query(filters.regex(r"cspeed_(.+)_(.*)"))
async def channel_speed_callback(client, callback_query):
    """Handle channel speed button callbacks"""
    speed_str = callback_query.data.split("_")[1]
    channel_id = int(callback_query.data.split("_")[2])
    
    try:
        speed = float(speed_str)
        SPEED_SETTINGS[f"channel_{channel_id}"] = speed
        
        await callback_query.answer(f"⚡ Channel speed set to {speed}x", show_alert=False)
        await callback_query.message.edit_text(
            f"⚡ **Channel Speed Set to {speed}x**\n\n"
            f"⚠️ **Note:** Channel speed control is under development."
        )
        
    except ValueError:
        await callback_query.answer("❌ Invalid speed value", show_alert=True)

@app.on_message(filters.command(["speedreset"]) & filters.group )
@AdminRightsCheck
async def speed_reset(client, message: Message, _, chat_id):
    """Reset speed to normal (1x)"""
    
    SPEED_SETTINGS[chat_id] = 1.0
    
    await message.reply_text(
        "🔄 **Speed Reset to Normal**\n\n"
        "**Current Speed:** 1x (Normal)\n\n"
        "Playback speed has been reset to default."
    )

@app.on_message(filters.command(["speedinfo"]) & filters.group )
async def speed_info(client, message: Message):
    """Show current speed information"""
    
    chat_id = message.chat.id
    current_speed = SPEED_SETTINGS.get(chat_id, 1.0)
    
    # Speed descriptions
    if current_speed < 0.75:
        description = "🐌 Very Slow"
        effect = "Audio will play much slower than normal"
    elif current_speed < 1.0:
        description = "🚶 Slow"
        effect = "Audio will play slower than normal"
    elif current_speed == 1.0:
        description = "🎵 Normal"
        effect = "Audio will play at normal speed"
    elif current_speed <= 1.5:
        description = "🏃 Fast"
        effect = "Audio will play faster than normal"
    else:
        description = "🚀 Very Fast"
        effect = "Audio will play much faster than normal"
    
    await message.reply_text(
        f"⚡ **Speed Information**\n\n"
        f"**Current Speed:** {current_speed}x\n"
        f"**Mode:** {description}\n"
        f"**Effect:** {effect}\n\n"
        f"**Available Commands:**\n"
        f"• `/speed <rate>` - Set custom speed\n"
        f"• `/speedreset` - Reset to normal speed\n"
        f"• `/cspeed <rate>` - Set channel speed"
    )

def get_speed_setting(chat_id: int) -> float:
    """Get speed setting for a chat"""
    return SPEED_SETTINGS.get(chat_id, 1.0)