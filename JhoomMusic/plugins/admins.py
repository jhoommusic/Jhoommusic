from pyrogram import filters
from pyrogram.types import Message

from JhoomMusic import app
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.decorators import AdminRightsCheck
from config import BANNED_USERS


@app.on_message(filters.command(["pause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/pause`")
    
    try:
        await Jhoom.pause_stream(chat_id)
        await message.reply_text("⏸️ **Music paused!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")


@app.on_message(filters.command(["resume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_admin(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/resume`")
    
    try:
        await Jhoom.resume_stream(chat_id)
        await message.reply_text("▶️ **Music resumed!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")


@app.on_message(filters.command(["stop", "end"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def stop_admin(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/stop`")
    
    try:
        await Jhoom.stop_stream(chat_id)
        await message.reply_text("⏹️ **Music stopped and queue cleared!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")


@app.on_message(filters.command(["skip", "next"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def skip_admin(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/skip`")
    
    try:
        await Jhoom.stop_stream(chat_id)
        await message.reply_text("⏭️ **Skipped to next song!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")


@app.on_message(filters.command(["mute"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def mute_admin(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/mute`")
    
    try:
        await Jhoom.mute_stream(chat_id)
        await message.reply_text("🔇 **Assistant muted!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")


@app.on_message(filters.command(["unmute"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def unmute_admin(client, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/unmute`")
    
    try:
        await Jhoom.unmute_stream(chat_id)
        await message.reply_text("🔊 **Assistant unmuted!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")