from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from JhoomMusic import app
from config import BANNED_USERS, START_IMG_URL, BOT_NAME, SUPPORT_CHAT, SUPPORT_CHANNEL

START_TEXT = f"""
🎵 **Welcome to {BOT_NAME}!**

I'm a powerful music bot that can play high-quality music in your Telegram groups!

**🔥 Features:**
• Play music from YouTube
• High quality audio streaming
• Queue management
• Admin controls
• Live stream support
• Video calls support

**📚 Quick Commands:**
• `/play <song name>` - Play a song
• `/commands` - Show all commands
• `/help` - Get help

**💡 How to use:**
1. Add me to your group
2. Make me admin with necessary permissions
3. Use `/play <song name>` to start playing music!

**🆘 Need help?** Join our [Support Chat]({SUPPORT_CHAT})
"""

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
async def start_pm(client, message: Message):
    """Handle /start command in private chat"""
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=START_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "➕ Add me to your Group ➕",
                    url=f"https://t.me/{app.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton("🎵 Commands", callback_data="back_to_commands"),
                InlineKeyboardButton("ℹ️ About", callback_data="about_bot")
            ],
            [
                InlineKeyboardButton("🆘 Support", url=SUPPORT_CHAT),
                InlineKeyboardButton("📢 Updates", url=SUPPORT_CHANNEL),
            ]
        ])
    )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
async def start_gp(client, message: Message):
    """Handle /start command in group chat"""
    out = f"""
🎵 **{BOT_NAME} Started Successfully!**

**🔥 I'm ready to play music in this group!**

**📚 Basic Commands:**
• `/play <song name>` - Play music
• `/pause` - Pause current song
• `/resume` - Resume paused song
• `/skip` - Skip current song
• `/stop` - Stop playing
• `/commands` - Show all commands

**💡 Make sure I have admin permissions to work properly!**
"""
    
    await message.reply_text(
        text=out,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 All Commands", callback_data="back_to_commands"),
                InlineKeyboardButton("⚡ Quick Help", callback_data="quick_help_group")
            ],
            [
                InlineKeyboardButton("🆘 Support", url=SUPPORT_CHAT),
                InlineKeyboardButton("📢 Updates", url=SUPPORT_CHANNEL),
            ]
        ])
    )

@app.on_callback_query(filters.regex("quick_help_group"))
async def quick_help_group(client, callback_query):
    """Show quick help in group context"""
    
    quick_text = f"""
**⚡ QUICK HELP - {BOT_NAME}**

**🎵 Music Commands:**
• `/play <song>` - Play music
• `/pause` - Pause playback
• `/resume` - Resume playback
• `/skip` - Skip current song
• `/stop` - Stop and clear queue
• `/queue` - Show current queue

**👑 Admin Commands:**
• `/auth <user>` - Authorize user
• `/mute` - Mute assistant
• `/unmute` - Unmute assistant
• `/shuffle` - Shuffle queue
• `/clearqueue` - Clear queue

**📊 Info Commands:**
• `/ping` - Check bot status
• `/nowplaying` - Current track info

**For complete command list, use** `/commands`
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📋 All Commands", callback_data="back_to_commands"),
            InlineKeyboardButton("🔙 Back", callback_data="back_to_start_group")
        ]
    ]
    
    await callback_query.message.edit_text(
        quick_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@app.on_callback_query(filters.regex("back_to_start_group"))
async def back_to_start_group(client, callback_query):
    """Go back to group start message"""
    
    out = f"""
🎵 **{BOT_NAME} Started Successfully!**

**🔥 I'm ready to play music in this group!**

**📚 Basic Commands:**
• `/play <song name>` - Play music
• `/pause` - Pause current song
• `/resume` - Resume paused song
• `/skip` - Skip current song
• `/stop` - Stop playing
• `/commands` - Show all commands

**💡 Make sure I have admin permissions to work properly!**
"""
    
    await callback_query.message.edit_text(
        text=out,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 All Commands", callback_data="back_to_commands"),
                InlineKeyboardButton("⚡ Quick Help", callback_data="quick_help_group")
            ],
            [
                InlineKeyboardButton("🆘 Support", url=SUPPORT_CHAT),
                InlineKeyboardButton("📢 Updates", url=SUPPORT_CHANNEL),
            ]
        ])
    )

@app.on_message(filters.command(["help"]) & ~BANNED_USERS)
async def help_com(client, message: Message):
    """Handle /help command - redirect to commands"""
    await message.reply_text(
        f"**📋 For complete command list, use** `/commands`\n\n"
        f"**⚡ For quick help, use** `/quickhelp`",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 All Commands", callback_data="back_to_commands"),
                InlineKeyboardButton("⚡ Quick Help", callback_data="show_quick_help")
            ]
        ])
    )

@app.on_callback_query(filters.regex("show_quick_help"))
async def show_quick_help_callback(client, callback_query):
    """Show quick help via callback"""
    
    quick_text = f"""
**⚡ QUICK HELP - {BOT_NAME}**

**🎵 Essential Commands:**
• `/play <song>` - Play music
• `/pause` - Pause playback
• `/resume` - Resume playback
• `/skip` - Skip current song
• `/stop` - Stop and clear queue

**👑 Admin Commands:**
• `/auth <user>` - Authorize user
• `/mute` - Mute assistant
• `/clearqueue` - Clear queue

**📊 Info Commands:**
• `/ping` - Check bot status
• `/queue` - Show current queue

**Need more commands?** Use `/commands` for full list!
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📋 All Commands", callback_data="back_to_commands"),
            InlineKeyboardButton("🆘 Support", url=SUPPORT_CHAT)
        ]
    ]
    
    await callback_query.message.edit_text(
        quick_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )