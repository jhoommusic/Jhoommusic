from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from JhoomMusic import app
from JhoomMusic.utils.database import get_lang, is_on_off
from config import BANNED_USERS, START_IMG_URL, BOT_NAME, SUPPORT_CHAT


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
async def start_pm(client, message: Message):
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=f"""**🎵 Welcome to {BOT_NAME}!**

I'm a powerful music bot that can play music in your Telegram groups!

**🔥 Features:**
• Play music from YouTube
• High quality audio streaming
• Queue management
• Admin controls
• Live stream support
• Video calls support

**📚 Commands:**
• `/play` - Play a song
• `/pause` - Pause current song
• `/resume` - Resume paused song
• `/skip` - Skip current song
• `/stop` - Stop playing and clear queue
• `/queue` - Show current queue

**💡 How to use:**
1. Add me to your group
2. Make me admin with necessary permissions
3. Use `/play <song name>` to start playing music!

**🆘 Need help?** Join our [Support Chat]({SUPPORT_CHAT})""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add me to your Group ➕",
                        url=f"https://t.me/{app.username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton("🆘 Support", url=SUPPORT_CHAT),
                    InlineKeyboardButton("📢 Updates", url="https://t.me/JhoomMusicChannel"),
                ],
                [
                    InlineKeyboardButton("🔧 Commands", callback_data="settings_back_helper"),
                ],
            ]
        ),
    )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
async def start_gp(client, message: Message):
    out = f"""**🎵 {BOT_NAME} Started Successfully!**

**🔥 I'm ready to play music in this group!**

**📚 Basic Commands:**
• `/play <song name>` - Play music
• `/pause` - Pause current song
• `/resume` - Resume paused song
• `/skip` - Skip current song
• `/stop` - Stop playing

**💡 Make sure I have admin permissions to work properly!**"""
    
    await message.reply_text(
        text=out,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🆘 Support", url=SUPPORT_CHAT),
                    InlineKeyboardButton("📢 Updates", url="https://t.me/JhoomMusicChannel"),
                ]
            ]
        ),
    )


@app.on_message(filters.command(["help"]) & ~BANNED_USERS)
async def help_com(client, message: Message):
    await message.reply_text(
        f"""**🆘 Help Menu for {BOT_NAME}**

**🎵 Music Commands:**
• `/play <song name>` - Play music from YouTube
• `/pause` - Pause the current song
• `/resume` - Resume the paused song
• `/skip` - Skip to next song in queue
• `/stop` - Stop playing and clear queue
• `/queue` - Show current queue
• `/shuffle` - Shuffle the queue

**👥 Admin Commands:**
• `/auth <username>` - Add user to auth list
• `/unauth <username>` - Remove user from auth list
• `/authusers` - Show authorized users
• `/pause`, `/resume`, `/skip`, `/stop` - Control playback

**⚙️ Settings Commands:**
• `/settings` - Open settings panel
• `/language` - Change bot language

**📊 Other Commands:**
• `/ping` - Check bot ping
• `/stats` - Show bot statistics

**💡 Note:** Some commands require admin permissions in the group.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🆘 Support", url=SUPPORT_CHAT),
                    InlineKeyboardButton("📢 Updates", url="https://t.me/JhoomMusicChannel"),
                ]
            ]
        ),
    )