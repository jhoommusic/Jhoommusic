from pyrogram import filters
from pyrogram.types import Message

from JhoomMusic import app
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.decorators import AdminRightsCheck
from config import BANNED_USERS

@app.on_message(filters.command(["pause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(client, message: Message, _, chat_id):
    """Pause the current stream"""
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/pause`")
    
    try:
        success = await Jhoom.pause_stream(chat_id)
        if success:
            await message.reply_text("⏸️ **Music paused!**")
        else:
            await message.reply_text("❌ **No active stream to pause**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["resume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_admin(client, message: Message, _, chat_id):
    """Resume the paused stream"""
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/resume`")
    
    try:
        success = await Jhoom.resume_stream(chat_id)
        if success:
            await message.reply_text("▶️ **Music resumed!**")
        else:
            await message.reply_text("❌ **No paused stream to resume**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["stop", "end"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def stop_admin(client, message: Message, _, chat_id):
    """Stop the current stream"""
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/stop`")
    
    try:
        success = await Jhoom.stop_stream(chat_id)
        if success:
            await message.reply_text("⏹️ **Music stopped and queue cleared!**")
        else:
            await message.reply_text("❌ **No active stream to stop**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["skip", "next"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def skip_admin(client, message: Message, _, chat_id):
    """Skip to next track"""
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/skip`")
    
    try:
        # Import queues from play.py
        from JhoomMusic.plugins.play import queues
        
        if chat_id in queues and queues[chat_id]:
            next_track = queues[chat_id].pop(0)
            success = await Jhoom.skip_stream(chat_id, next_track["file"])
            if success:
                await message.reply_text(f"⏭️ **Skipped to:** {next_track['title']}")
            else:
                await message.reply_text("❌ **Failed to skip**")
        else:
            success = await Jhoom.stop_stream(chat_id)
            if success:
                await message.reply_text("⏭️ **No more tracks, playback stopped!**")
            else:
                await message.reply_text("❌ **No active stream**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["mute"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def mute_admin(client, message: Message, _, chat_id):
    """Mute the stream"""
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/mute`")
    
    try:
        success = await Jhoom.mute_stream(chat_id)
        if success:
            await message.reply_text("🔇 **Assistant muted!**")
        else:
            await message.reply_text("❌ **No active stream to mute**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["unmute"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def unmute_admin(client, message: Message, _, chat_id):
    """Unmute the stream"""
    if not len(message.command) == 1:
        return await message.reply_text("**Usage:** `/unmute`")
    
    try:
        success = await Jhoom.unmute_stream(chat_id)
        if success:
            await message.reply_text("🔊 **Assistant unmuted!**")
        else:
            await message.reply_text("❌ **No muted stream to unmute**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["queue", "q"]) & filters.group & ~BANNED_USERS)
async def show_queue(client, message: Message):
    """Show current queue"""
    chat_id = message.chat.id
    
    try:
        # Import queues from play.py
        from JhoomMusic.plugins.play import queues
        
        if chat_id in queues and queues[chat_id]:
            queue_text = "🎵 **Current Queue:**\n\n"
            for i, track in enumerate(queues[chat_id][:10], 1):
                queue_text += f"{i}. **{track['title']}**\n   👤 Requested by: {track['user']}\n\n"
            
            if len(queues[chat_id]) > 10:
                queue_text += f"... and **{len(queues[chat_id]) - 10}** more tracks"
            
            await message.reply_text(queue_text)
        else:
            await message.reply_text("📭 **Queue is empty**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["shuffle"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def shuffle_queue(client, message: Message, _, chat_id):
    """Shuffle the queue"""
    try:
        # Import queues from play.py
        from JhoomMusic.plugins.play import queues
        import random
        
        if chat_id in queues and queues[chat_id]:
            random.shuffle(queues[chat_id])
            await message.reply_text("🔀 **Queue shuffled!**")
        else:
            await message.reply_text("📭 **No tracks in queue to shuffle**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["clearqueue", "clear"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def clear_queue(client, message: Message, _, chat_id):
    """Clear the queue"""
    try:
        # Import queues from play.py
        from JhoomMusic.plugins.play import queues
        
        if chat_id in queues:
            queues[chat_id].clear()
            await message.reply_text("🗑️ **Queue cleared!**")
        else:
            await message.reply_text("📭 **Queue is already empty**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")