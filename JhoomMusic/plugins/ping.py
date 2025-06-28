import time
from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from JhoomMusic import app
from config import BANNED_USERS, PING_IMG_URL, BOT_NAME


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
async def ping_pong(client, message: Message):
    start = time.time()
    response = await message.reply_text("🏓 **Pinging...**")
    end = time.time()
    
    ping_time = round((end - start) * 1000, 2)
    uptime = datetime.now() - datetime.fromtimestamp(time.time() - time.process_time())
    
    await response.edit_text(
        f"🏓 **Pong!**\n\n"
        f"📊 **Bot Statistics:**\n"
        f"• **Ping:** `{ping_time}ms`\n"
        f"• **Uptime:** `{str(uptime).split('.')[0]}`\n"
        f"• **Bot Name:** {BOT_NAME}\n"
        f"• **Python Version:** `3.9+`\n"
        f"• **Pyrogram Version:** `2.0.106`\n"
        f"• **PyTgCalls Version:** `0.9.7`",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🆘 Support", url="https://t.me/JhoomMusicSupport"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/JhoomMusicChannel")
            ]
        ])
    )