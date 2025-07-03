import asyncio
import os
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from tgcaller.exceptions import NoActiveGroupCall, TelegramServerError

from JhoomMusic import app, userbot
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.decorators import AdminRightsCheck
from JhoomMusic.utils.formatters import seconds_to_min
from JhoomMusic.utils.stream import get_track_info, ytsearch
from config import BANNED_USERS, BOT_NAME, DURATION_LIMIT_MIN

# Global queue storage
queues = {}

@app.on_message(filters.command(["play", "p"]) & filters.group & ~BANNED_USERS)
async def play_command(client, message: Message):
    """Handle /play command"""
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/play <song name or YouTube link>`\n\n"
            "**Examples:**\n"
            "• `/play Imagine Dragons Believer`\n"
            "• `/play https://youtu.be/dQw4w9WgXcQ`"
        )
    
    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    mystic = await message.reply_text("🔍 **Searching for your song...**")
    
    try:
        # Get track information
        track_info = await get_track_info(query)
        
        if not track_info:
            return await mystic.edit_text(
                "❌ **No results found!**\n\n"
                "Try a different search term or check if the link is valid."
            )
        
        # Check duration limit
        duration = track_info.get("duration", 0)
        if duration and duration > (DURATION_LIMIT_MIN * 60):
            return await mystic.edit_text(
                f"❌ **Duration Error**\n\n"
                f"**Track Duration:** {seconds_to_min(duration)}\n"
                f"**Limit:** {DURATION_LIMIT_MIN} minutes"
            )
        
        await mystic.edit_text("📥 **Processing your request...**")
        
        # Prepare track data
        track_data = {
            "title": track_info["title"],
            "file": track_info["url"],
            "duration": duration,
            "user": user_name,
            "user_id": user_id,
            "videoid": track_info.get("videoid", ""),
            "thumbnail": track_info.get("thumbnail", ""),
            "source": track_info.get("source", "youtube")
        }
        
        # Check if already playing
        try:
            # Try to join the voice chat
            success = await Jhoom.join_call(
                chat_id,
                chat_id,
                track_info["url"],
                video=False
            )
            
            if success:
                # Add to current playing
                if chat_id not in queues:
                    queues[chat_id] = []
                
                await mystic.edit_text(
                    f"🎵 **Now Playing**\n\n"
                    f"**Title:** {track_info['title']}\n"
                    f"**Duration:** {seconds_to_min(duration) if duration else 'Unknown'}\n"
                    f"**Requested by:** {user_name}",
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}"),
                            InlineKeyboardButton("⏭️ Skip", callback_data=f"skip_{chat_id}"),
                            InlineKeyboardButton("⏹️ Stop", callback_data=f"stop_{chat_id}")
                        ],
                        [
                            InlineKeyboardButton("🔄 Queue", callback_data=f"queue_{chat_id}"),
                            InlineKeyboardButton("❌ Close", callback_data="close")
                        ]
                    ])
                )
            else:
                await mystic.edit_text(
                    "❌ **Failed to join voice chat!**\n\n"
                    "Make sure:\n"
                    "• Voice chat is active\n"
                    "• Bot has admin permissions\n"
                    "• Bot can manage voice chats"
                )
            
        except NoActiveGroupCall:
            return await mystic.edit_text(
                "❌ **Voice chat is not active!**\n\n"
                "Please start a voice chat first and try again."
            )
        except TelegramServerError:
            return await mystic.edit_text(
                "❌ **Telegram Server Error!**\n\n"
                "Please try again later."
            )
        except Exception as e:
            return await mystic.edit_text(f"❌ **Playback Error:** {str(e)}")
            
    except Exception as e:
        return await mystic.edit_text(f"❌ **Unexpected Error:** {str(e)}")

@app.on_message(filters.command(["vplay", "videoplay"]) & filters.group & ~BANNED_USERS)
async def video_play_command(client, message: Message):
    """Handle /vplay command for video playback"""
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/vplay <video name or YouTube link>`"
        )
    
    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    mystic = await message.reply_text("🔍 **Searching for your video...**")
    
    try:
        # Get track information
        track_info = await get_track_info(query)
        
        if not track_info:
            return await mystic.edit_text("❌ **No results found!**")
        
        await mystic.edit_text("📥 **Processing your video request...**")
        
        # Try to join the voice chat with video
        try:
            success = await Jhoom.join_call(
                chat_id,
                chat_id,
                track_info["url"],
                video=True
            )
            
            if success:
                await mystic.edit_text(
                    f"🎬 **Now Playing Video**\n\n"
                    f"**Title:** {track_info['title']}\n"
                    f"**Requested by:** {user_name}",
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}"),
                            InlineKeyboardButton("⏹️ Stop", callback_data=f"stop_{chat_id}")
                        ]
                    ])
                )
            else:
                await mystic.edit_text("❌ **Failed to start video playback!**")
            
        except Exception as e:
            return await mystic.edit_text(f"❌ **Video Playback Error:** {str(e)}")
            
    except Exception as e:
        return await mystic.edit_text(f"❌ **Error:** {str(e)}")

# Callback handlers for inline buttons
@app.on_callback_query(filters.regex(r"pause_(.*)"))
async def pause_callback(client, callback_query):
    """Handle pause button"""
    chat_id = int(callback_query.data.split("_")[1])
    
    try:
        success = await Jhoom.pause_stream(chat_id)
        if success:
            await callback_query.answer("⏸️ Paused!", show_alert=False)
            
            # Update button
            keyboard = callback_query.message.reply_markup.inline_keyboard
            keyboard[0][0] = InlineKeyboardButton("▶️ Resume", callback_data=f"resume_{chat_id}")
            
            await callback_query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await callback_query.answer("❌ Failed to pause", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex(r"resume_(.*)"))
async def resume_callback(client, callback_query):
    """Handle resume button"""
    chat_id = int(callback_query.data.split("_")[1])
    
    try:
        success = await Jhoom.resume_stream(chat_id)
        if success:
            await callback_query.answer("▶️ Resumed!", show_alert=False)
            
            # Update button
            keyboard = callback_query.message.reply_markup.inline_keyboard
            keyboard[0][0] = InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}")
            
            await callback_query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await callback_query.answer("❌ Failed to resume", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex(r"skip_(.*)"))
async def skip_callback(client, callback_query):
    """Handle skip button"""
    chat_id = int(callback_query.data.split("_")[1])
    
    try:
        # Check if there are tracks in queue
        if chat_id in queues and queues[chat_id]:
            next_track = queues[chat_id].pop(0)
            success = await Jhoom.skip_stream(chat_id, next_track["file"])
            if success:
                await callback_query.answer("⏭️ Skipped!", show_alert=False)
                await callback_query.message.edit_text(
                    f"⏭️ **Skipped to:** {next_track['title']}"
                )
            else:
                await callback_query.answer("❌ Failed to skip", show_alert=True)
        else:
            # No more tracks, stop playback
            success = await Jhoom.stop_stream(chat_id)
            if success:
                await callback_query.answer("⏭️ No more tracks, stopped!", show_alert=False)
                await callback_query.message.edit_text("⏹️ **Playback ended - no more tracks in queue**")
            else:
                await callback_query.answer("❌ Failed to skip", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex(r"stop_(.*)"))
async def stop_callback(client, callback_query):
    """Handle stop button"""
    chat_id = int(callback_query.data.split("_")[1])
    
    try:
        success = await Jhoom.stop_stream(chat_id)
        if success:
            # Clear queue
            if chat_id in queues:
                queues[chat_id].clear()
            
            await callback_query.answer("⏹️ Stopped!", show_alert=False)
            await callback_query.message.edit_text("⏹️ **Music stopped and queue cleared!**")
        else:
            await callback_query.answer("❌ Failed to stop", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex(r"queue_(.*)"))
async def queue_callback(client, callback_query):
    """Handle queue button"""
    chat_id = int(callback_query.data.split("_")[1])
    
    try:
        if chat_id in queues and queues[chat_id]:
            queue_text = "🎵 **Current Queue:**\n\n"
            for i, track in enumerate(queues[chat_id][:10], 1):
                queue_text += f"{i}. {track['title']}\n"
            
            if len(queues[chat_id]) > 10:
                queue_text += f"\n... and {len(queues[chat_id]) - 10} more tracks"
            
            await callback_query.answer(queue_text, show_alert=True)
        else:
            await callback_query.answer("📭 Queue is empty", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex("close"))
async def close_callback(client, callback_query):
    """Handle close button"""
    await callback_query.message.delete()
    await callback_query.answer("❌ Closed!", show_alert=False)