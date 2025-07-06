from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus

from JhoomMusic import app, userbot
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.decorators import AdminRightsCheck
from JhoomMusic.utils.stream import get_track_info
from JhoomMusic.utils.formatters import seconds_to_min
from config import BANNED_USERS, DURATION_LIMIT_MIN

# Store channel connections
CHANNEL_CONNECTIONS = {}

@app.on_message(filters.command(["channelplay", "cplay"]) & filters.group )
@AdminRightsCheck
async def channel_play_command(client, message: Message, _, chat_id):
    """Connect channel to group for music streaming"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/channelplay <channel_username>` - Connect channel\n"
            "• `/channelplay <channel_id>` - Connect channel by ID\n\n"
            "**Examples:**\n"
            "• `/channelplay @mychannel`\n"
            "• `/channelplay -1001234567890`"
        )
    
    channel_input = message.command[1]
    
    try:
        # Get channel info
        if channel_input.startswith("@"):
            channel = await app.get_chat(channel_input)
        else:
            channel_id = int(channel_input)
            channel = await app.get_chat(channel_id)
        
        channel_id = channel.id
        channel_name = channel.title
        
        # Check if bot is admin in channel
        try:
            bot_member = await app.get_chat_member(channel_id, app.id)
            if bot_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await message.reply_text(
                    f"❌ **Bot is not admin in {channel_name}!**\n\n"
                    "Please make the bot admin in the channel first."
                )
        except:
            return await message.reply_text(
                f"❌ **Cannot access channel {channel_name}!**\n\n"
                "Make sure the bot is added to the channel as admin."
            )
        
        # Connect channel to group
        CHANNEL_CONNECTIONS[chat_id] = {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "connected_by": message.from_user.id
        }
        
        await message.reply_text(
            f"✅ **Channel Connected!**\n\n"
            f"**Channel:** {channel_name}\n"
            f"**ID:** `{channel_id}`\n\n"
            f"**Now you can use `/cplay` to stream music in the channel.**",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🎵 Play Music", callback_data=f"cplay_music_{chat_id}"),
                    InlineKeyboardButton("❌ Disconnect", callback_data=f"disconnect_channel_{chat_id}")
                ]
            ])
        )
        
    except ValueError:
        await message.reply_text("❌ **Invalid channel ID!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["cplay"]) & filters.group )
async def channel_audio_play(client, message: Message):
    """Stream audio in connected channel"""
    
    chat_id = message.chat.id
    
    # Check if channel is connected
    if chat_id not in CHANNEL_CONNECTIONS:
        return await message.reply_text(
            "❌ **No channel connected!**\n\n"
            "Use `/channelplay @channel` to connect a channel first."
        )
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/cplay <song name or link>`\n\n"
            "**Example:** `/cplay Imagine Dragons Believer`"
        )
    
    query = " ".join(message.command[1:])
    channel_info = CHANNEL_CONNECTIONS[chat_id]
    channel_id = channel_info["channel_id"]
    channel_name = channel_info["channel_name"]
    
    mystic = await message.reply_text(f"🔍 **Searching for:** {query}")
    
    try:
        # Get track information
        track_info = await get_track_info(query)
        
        if not track_info:
            return await mystic.edit_text("❌ **No results found!**")
        
        # Check duration limit
        duration = track_info.get("duration", 0)
        if duration and duration > (DURATION_LIMIT_MIN * 60):
            return await mystic.edit_text(
                f"❌ **Duration Error**\n\n"
                f"**Track Duration:** {seconds_to_min(duration)}\n"
                f"**Limit:** {DURATION_LIMIT_MIN} minutes"
            )
        
        await mystic.edit_text("📥 **Starting channel stream...**")
        
        # Start streaming in channel
        success = await Jhoom.join_call(
            channel_id,
            chat_id,
            track_info["url"],
            video=False
        )
        
        if success:
            await mystic.edit_text(
                f"🎵 **Now Streaming in Channel**\n\n"
                f"**Channel:** {channel_name}\n"
                f"**Track:** {track_info['title']}\n"
                f"**Duration:** {seconds_to_min(duration) if duration else 'Unknown'}\n"
                f"**Requested by:** {message.from_user.first_name}",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("⏸️ Pause", callback_data=f"cpause_{channel_id}"),
                        InlineKeyboardButton("⏹️ Stop", callback_data=f"cstop_{channel_id}")
                    ],
                    [
                        InlineKeyboardButton("❌ Close", callback_data="close")
                    ]
                ])
            )
        else:
            await mystic.edit_text(
                f"❌ **Failed to start stream in {channel_name}!**\n\n"
                "Make sure voice chat is active in the channel."
            )
        
    except Exception as e:
        await mystic.edit_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["cvplay"]) & filters.group )
async def channel_video_play(client, message: Message):
    """Stream video in connected channel"""
    
    chat_id = message.chat.id
    
    # Check if channel is connected
    if chat_id not in CHANNEL_CONNECTIONS:
        return await message.reply_text(
            "❌ **No channel connected!**\n\n"
            "Use `/channelplay @channel` to connect a channel first."
        )
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/cvplay <video name or link>`\n\n"
            "**Example:** `/cvplay Imagine Dragons Believer`"
        )
    
    query = " ".join(message.command[1:])
    channel_info = CHANNEL_CONNECTIONS[chat_id]
    channel_id = channel_info["channel_id"]
    channel_name = channel_info["channel_name"]
    
    mystic = await message.reply_text(f"🔍 **Searching for video:** {query}")
    
    try:
        # Get track information
        track_info = await get_track_info(query)
        
        if not track_info:
            return await mystic.edit_text("❌ **No results found!**")
        
        await mystic.edit_text("📥 **Starting video stream...**")
        
        # Start video streaming in channel
        success = await Jhoom.join_call(
            channel_id,
            chat_id,
            track_info["url"],
            video=True
        )
        
        if success:
            await mystic.edit_text(
                f"🎬 **Now Streaming Video in Channel**\n\n"
                f"**Channel:** {channel_name}\n"
                f"**Video:** {track_info['title']}\n"
                f"**Requested by:** {message.from_user.first_name}",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("⏸️ Pause", callback_data=f"cpause_{channel_id}"),
                        InlineKeyboardButton("⏹️ Stop", callback_data=f"cstop_{channel_id}")
                    ]
                ])
            )
        else:
            await mystic.edit_text(
                f"❌ **Failed to start video stream in {channel_name}!**"
            )
        
    except Exception as e:
        await mystic.edit_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["cplayforce"]) & filters.group )
@AdminRightsCheck
async def channel_force_play(client, message: Message, _, chat_id):
    """Force play new track in channel"""
    
    # Check if channel is connected
    if chat_id not in CHANNEL_CONNECTIONS:
        return await message.reply_text(
            "❌ **No channel connected!**\n\n"
            "Use `/channelplay @channel` to connect a channel first."
        )
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/cplayforce <song name or link>`"
        )
    
    query = " ".join(message.command[1:])
    channel_info = CHANNEL_CONNECTIONS[chat_id]
    channel_id = channel_info["channel_id"]
    channel_name = channel_info["channel_name"]
    
    mystic = await message.reply_text(f"🔍 **Force playing:** {query}")
    
    try:
        # Get track information
        track_info = await get_track_info(query)
        
        if not track_info:
            return await mystic.edit_text("❌ **No results found!**")
        
        await mystic.edit_text("📥 **Force starting stream...**")
        
        # Stop current stream and start new one
        await Jhoom.stop_stream(channel_id)
        
        success = await Jhoom.join_call(
            channel_id,
            chat_id,
            track_info["url"],
            video=False
        )
        
        if success:
            await mystic.edit_text(
                f"⚡ **Force Playing in Channel**\n\n"
                f"**Channel:** {channel_name}\n"
                f"**Track:** {track_info['title']}\n"
                f"**Requested by:** {message.from_user.first_name}"
            )
        else:
            await mystic.edit_text(f"❌ **Failed to force play in {channel_name}!**")
        
    except Exception as e:
        await mystic.edit_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["channelstop", "cstop"]) & filters.group )
@AdminRightsCheck
async def channel_stop(client, message: Message, _, chat_id):
    """Stop channel streaming"""
    
    # Check if channel is connected
    if chat_id not in CHANNEL_CONNECTIONS:
        return await message.reply_text("❌ **No channel connected!**")
    
    channel_info = CHANNEL_CONNECTIONS[chat_id]
    channel_id = channel_info["channel_id"]
    channel_name = channel_info["channel_name"]
    
    try:
        success = await Jhoom.stop_stream(channel_id)
        if success:
            await message.reply_text(f"⏹️ **Stopped streaming in {channel_name}**")
        else:
            await message.reply_text(f"❌ **No active stream in {channel_name}**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["channeldisconnect", "cdisconnect"]) & filters.group )
@AdminRightsCheck
async def disconnect_channel(client, message: Message, _, chat_id):
    """Disconnect channel from group"""
    
    if chat_id not in CHANNEL_CONNECTIONS:
        return await message.reply_text("❌ **No channel connected!**")
    
    channel_info = CHANNEL_CONNECTIONS[chat_id]
    channel_name = channel_info["channel_name"]
    
    # Stop any active stream
    try:
        await Jhoom.stop_stream(channel_info["channel_id"])
    except:
        pass
    
    # Remove connection
    del CHANNEL_CONNECTIONS[chat_id]
    
    await message.reply_text(
        f"❌ **Channel Disconnected!**\n\n"
        f"**Channel:** {channel_name}\n\n"
        f"**Use `/channelplay` to connect a channel again.**"
    )

# Callback handlers for channel controls
@app.on_callback_query(filters.regex(r"cpause_(.*)"))
async def channel_pause_callback(client, callback_query):
    """Handle channel pause button"""
    channel_id = int(callback_query.data.split("_")[1])
    
    try:
        success = await Jhoom.pause_stream(channel_id)
        if success:
            await callback_query.answer("⏸️ Channel stream paused!", show_alert=False)
        else:
            await callback_query.answer("❌ Failed to pause", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex(r"cstop_(.*)"))
async def channel_stop_callback(client, callback_query):
    """Handle channel stop button"""
    channel_id = int(callback_query.data.split("_")[1])
    
    try:
        success = await Jhoom.stop_stream(channel_id)
        if success:
            await callback_query.answer("⏹️ Channel stream stopped!", show_alert=False)
            await callback_query.message.edit_text("⏹️ **Channel streaming stopped!**")
        else:
            await callback_query.answer("❌ Failed to stop", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex(r"disconnect_channel_(.*)"))
async def disconnect_channel_callback(client, callback_query):
    """Handle channel disconnect button"""
    chat_id = int(callback_query.data.split("_")[2])
    
    if chat_id in CHANNEL_CONNECTIONS:
        channel_info = CHANNEL_CONNECTIONS[chat_id]
        channel_name = channel_info["channel_name"]
        
        # Stop any active stream
        try:
            await Jhoom.stop_stream(channel_info["channel_id"])
        except:
            pass
        
        # Remove connection
        del CHANNEL_CONNECTIONS[chat_id]
        
        await callback_query.message.edit_text(
            f"❌ **Channel Disconnected!**\n\n"
            f"**Channel:** {channel_name}"
        )
        await callback_query.answer("Channel disconnected!", show_alert=False)
    else:
        await callback_query.answer("No channel connected!", show_alert=True)