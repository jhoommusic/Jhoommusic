from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from JhoomMusic import app
from JhoomMusic.utils.decorators import AdminRightsCheck
from config import BANNED_USERS

# Store loop settings for each chat
LOOP_SETTINGS = {}

@app.on_message(filters.command(["loop", "spiral"]) & filters.group )
@AdminRightsCheck
async def loop_command(client, message: Message, _, chat_id):
    """Control loop/spiral settings"""
    
    if len(message.command) == 1:
        # Show current loop status
        current_loop = LOOP_SETTINGS.get(chat_id, {"enabled": False, "count": 0})
        
        if current_loop["enabled"]:
            if current_loop["count"] == 0:
                status = "♾️ **Infinite Loop**"
            else:
                status = f"🔁 **Loop Count:** {current_loop['count']}"
        else:
            status = "❌ **Loop Disabled**"
        
        await message.reply_text(
            f"🌀 **Loop Status**\n\n{status}\n\n"
            f"**Usage:**\n"
            f"• `/loop enable` - Enable infinite loop\n"
            f"• `/loop disable` - Disable loop\n"
            f"• `/loop 1` - Loop once\n"
            f"• `/loop 5` - Loop 5 times\n"
            f"• `/loop 0` - Infinite loop",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔁 Enable", callback_data=f"loop_enable_{chat_id}"),
                    InlineKeyboardButton("❌ Disable", callback_data=f"loop_disable_{chat_id}")
                ],
                [
                    InlineKeyboardButton("1x", callback_data=f"loop_count_1_{chat_id}"),
                    InlineKeyboardButton("3x", callback_data=f"loop_count_3_{chat_id}"),
                    InlineKeyboardButton("5x", callback_data=f"loop_count_5_{chat_id}")
                ],
                [
                    InlineKeyboardButton("♾️ Infinite", callback_data=f"loop_infinite_{chat_id}")
                ]
            ])
        )
        return
    
    option = message.command[1].lower()
    
    if option in ["enable", "on", "true"]:
        # Enable infinite loop
        LOOP_SETTINGS[chat_id] = {"enabled": True, "count": 0}
        await message.reply_text(
            "♾️ **Infinite Loop Enabled!**\n\n"
            "Current track will repeat infinitely until stopped."
        )
    
    elif option in ["disable", "off", "false"]:
        # Disable loop
        LOOP_SETTINGS[chat_id] = {"enabled": False, "count": 0}
        await message.reply_text(
            "❌ **Loop Disabled!**\n\n"
            "Tracks will play normally without repeating."
        )
    
    else:
        # Try to parse as number
        try:
            count = int(option)
            if count < 0:
                return await message.reply_text("❌ **Loop count cannot be negative!**")
            
            if count == 0:
                # Infinite loop
                LOOP_SETTINGS[chat_id] = {"enabled": True, "count": 0}
                await message.reply_text(
                    "♾️ **Infinite Loop Enabled!**\n\n"
                    "Current track will repeat infinitely."
                )
            else:
                # Specific count
                LOOP_SETTINGS[chat_id] = {"enabled": True, "count": count}
                await message.reply_text(
                    f"🔁 **Loop Set to {count} times!**\n\n"
                    f"Current track will repeat {count} times."
                )
        
        except ValueError:
            await message.reply_text(
                "❌ **Invalid option!**\n\n"
                "**Usage:**\n"
                "• `/loop enable` - Enable infinite loop\n"
                "• `/loop disable` - Disable loop\n"
                "• `/loop <number>` - Set loop count"
            )

@app.on_callback_query(filters.regex(r"loop_enable_(.*)"))
async def loop_enable_callback(client, callback_query):
    """Handle loop enable callback"""
    chat_id = int(callback_query.data.split("_")[2])
    
    LOOP_SETTINGS[chat_id] = {"enabled": True, "count": 0}
    
    await callback_query.answer("♾️ Infinite loop enabled!", show_alert=False)
    await callback_query.message.edit_text(
        "♾️ **Infinite Loop Enabled!**\n\n"
        "Current track will repeat infinitely until stopped."
    )

@app.on_callback_query(filters.regex(r"loop_disable_(.*)"))
async def loop_disable_callback(client, callback_query):
    """Handle loop disable callback"""
    chat_id = int(callback_query.data.split("_")[2])
    
    LOOP_SETTINGS[chat_id] = {"enabled": False, "count": 0}
    
    await callback_query.answer("❌ Loop disabled!", show_alert=False)
    await callback_query.message.edit_text(
        "❌ **Loop Disabled!**\n\n"
        "Tracks will play normally without repeating."
    )

@app.on_callback_query(filters.regex(r"loop_count_(\d+)_(.*)"))
async def loop_count_callback(client, callback_query):
    """Handle loop count callback"""
    count = int(callback_query.data.split("_")[2])
    chat_id = int(callback_query.data.split("_")[3])
    
    LOOP_SETTINGS[chat_id] = {"enabled": True, "count": count}
    
    await callback_query.answer(f"🔁 Loop set to {count} times!", show_alert=False)
    await callback_query.message.edit_text(
        f"🔁 **Loop Set to {count} times!**\n\n"
        f"Current track will repeat {count} times."
    )

@app.on_callback_query(filters.regex(r"loop_infinite_(.*)"))
async def loop_infinite_callback(client, callback_query):
    """Handle infinite loop callback"""
    chat_id = int(callback_query.data.split("_")[2])
    
    LOOP_SETTINGS[chat_id] = {"enabled": True, "count": 0}
    
    await callback_query.answer("♾️ Infinite loop enabled!", show_alert=False)
    await callback_query.message.edit_text(
        "♾️ **Infinite Loop Enabled!**\n\n"
        "Current track will repeat infinitely until stopped."
    )

@app.on_message(filters.command(["loopinfo"]) & filters.group )
async def loop_info(client, message: Message):
    """Show detailed loop information"""
    
    chat_id = message.chat.id
    current_loop = LOOP_SETTINGS.get(chat_id, {"enabled": False, "count": 0})
    
    if current_loop["enabled"]:
        if current_loop["count"] == 0:
            status = "♾️ **Infinite Loop**"
            description = "The current track will repeat infinitely until manually stopped."
        else:
            status = f"🔁 **Loop Count: {current_loop['count']}**"
            description = f"The current track will repeat {current_loop['count']} times."
    else:
        status = "❌ **Loop Disabled**"
        description = "Tracks will play normally without repeating."
    
    await message.reply_text(
        f"🌀 **Loop Information**\n\n"
        f"{status}\n\n"
        f"**Description:** {description}\n\n"
        f"**Available Commands:**\n"
        f"• `/loop enable` - Enable infinite loop\n"
        f"• `/loop disable` - Disable loop\n"
        f"• `/loop <number>` - Set specific loop count\n"
        f"• `/loop 0` - Set infinite loop"
    )

def get_loop_setting(chat_id: int) -> dict:
    """Get loop setting for a chat"""
    return LOOP_SETTINGS.get(chat_id, {"enabled": False, "count": 0})

def should_loop(chat_id: int) -> bool:
    """Check if current track should loop"""
    loop_setting = get_loop_setting(chat_id)
    return loop_setting["enabled"]

def decrement_loop_count(chat_id: int) -> bool:
    """Decrement loop count and return if should continue looping"""
    if chat_id not in LOOP_SETTINGS:
        return False
    
    loop_setting = LOOP_SETTINGS[chat_id]
    
    if not loop_setting["enabled"]:
        return False
    
    if loop_setting["count"] == 0:  # Infinite loop
        return True
    
    if loop_setting["count"] > 1:
        LOOP_SETTINGS[chat_id]["count"] -= 1
        return True
    else:
        # Last loop, disable
        LOOP_SETTINGS[chat_id] = {"enabled": False, "count": 0}
        return False