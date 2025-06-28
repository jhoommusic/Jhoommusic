import asyncio
import os
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls.exceptions import NoActiveGroupCall, TelegramServerError
from yt_dlp import YoutubeDL

from JhoomMusic import app, userbot
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.database import is_on_off
from JhoomMusic.utils.decorators import AdminRightsCheck
from JhoomMusic.utils.formatters import seconds_to_min
from JhoomMusic.utils.inline import stream_markup, telegram_markup
from JhoomMusic.utils.stream import stream_from_link, ytsearch
from JhoomMusic.utils.database.queue import add_to_queue, get_queue
from config import BANNED_USERS, BOT_NAME, DURATION_LIMIT_MIN, SONG_DOWNLOAD_DURATION


@app.on_message(filters.command(["play", "p"]) & filters.group & ~BANNED_USERS)
async def play_commnd(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:** `/play <song name or YouTube link>`")
    
    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    mystic = await message.reply_text("🔍 **Searching for your song...**")
    
    try:
        # Check if it's a YouTube link
        if "youtube.com" in query or "youtu.be" in query:
            url = query
            try:
                with YoutubeDL({"quiet": True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get("title", "Unknown")
                    duration = info.get("duration", 0)
                    thumbnail = info.get("thumbnail", "")
                    videoid = info.get("id", "")
            except Exception as e:
                return await mystic.edit_text(f"❌ **Error:** Failed to extract video info\n\n**Details:** {str(e)}")
        else:
            # Search on YouTube
            try:
                results = ytsearch(query)
                if results == 0:
                    return await mystic.edit_text("❌ **No results found!** Try a different search term.")
                
                title, url, duration, thumbnail, videoid = results
            except Exception as e:
                return await mystic.edit_text(f"❌ **Search Error:** {str(e)}")
        
        # Check duration limit
        if duration and duration > (DURATION_LIMIT_MIN * 60):
            return await mystic.edit_text(
                f"❌ **Duration Error**\n\n**Track Duration:** {seconds_to_min(duration)}\n**Limit:** {DURATION_LIMIT_MIN} minutes"
            )
        
        await mystic.edit_text("📥 **Processing your request...**")
        
        # Get stream URL
        try:
            stream_url = await stream_from_link(url)
            if not stream_url:
                return await mystic.edit_text("❌ **Failed to get stream URL**")
        except Exception as e:
            return await mystic.edit_text(f"❌ **Stream Error:** {str(e)}")
        
        # Check if already playing
        try:
            await Jhoom.join_call(
                chat_id,
                chat_id,
                stream_url,
                video=False
            )
            
            await mystic.edit_text(
                f"🎵 **Now Playing**\n\n"
                f"**Title:** {title}\n"
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
            
        except NoActiveGroupCall:
            return await mystic.edit_text(
                "❌ **Voice chat is not active!**\n\nPlease start a voice chat first and try again."
            )
        except TelegramServerError:
            return await mystic.edit_text(
                "❌ **Telegram Server Error!**\n\nPlease try again later."
            )
        except Exception as e:
            return await mystic.edit_text(f"❌ **Playback Error:** {str(e)}")
            
    except Exception as e:
        return await mystic.edit_text(f"❌ **Unexpected Error:** {str(e)}")


@app.on_callback_query(filters.regex(r"pause_(.*)"))
async def pause_callback(client, callback_query):
    chat_id = int(callback_query.data.split("_")[1])
    
    try:
        await Jhoom.pause_stream(chat_id)
        await callback_query.answer("⏸️ Paused!", show_alert=False)
        
        # Update button
        keyboard = callback_query.message.reply_markup.inline_keyboard
        keyboard[0][0] = InlineKeyboardButton("▶️ Resume", callback_data=f"resume_{chat_id}")
        
        await callback_query.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)


@app.on_callback_query(filters.regex(r"resume_(.*)"))
async def resume_callback(client, callback_query):
    chat_id = int(callback_query.data.split("_")[1])
    
    try:
        await Jhoom.resume_stream(chat_id)
        await callback_query.answer("▶️ Resumed!", show_alert=False)
        
        # Update button
        keyboard = callback_query.message.reply_markup.inline_keyboard
        keyboard[0][0] = InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}")
        
        await callback_query.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)


@app.on_callback_query(filters.regex(r"skip_(.*)"))
async def skip_callback(client, callback_query):
    chat_id = int(callback_query.data.split("_")[1])
    
    try:
        await Jhoom.stop_stream(chat_id)
        await callback_query.answer("⏭️ Skipped!", show_alert=False)
        await callback_query.message.edit_text("⏭️ **Skipped to next song!**")
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)


@app.on_callback_query(filters.regex(r"stop_(.*)"))
async def stop_callback(client, callback_query):
    chat_id = int(callback_query.data.split("_")[1])
    
    try:
        await Jhoom.stop_stream(chat_id)
        await callback_query.answer("⏹️ Stopped!", show_alert=False)
        await callback_query.message.edit_text("⏹️ **Music stopped and queue cleared!**")
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)


@app.on_callback_query(filters.regex("close"))
async def close_callback(client, callback_query):
    await callback_query.message.delete()
    await callback_query.answer("❌ Closed!", show_alert=False)