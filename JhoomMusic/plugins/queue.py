from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from JhoomMusic import app
from JhoomMusic.utils.decorators import AdminRightsCheck
from JhoomMusic.utils.formatters import seconds_to_min
from config import BANNED_USERS

# Import queue from play.py
from JhoomMusic.plugins.play import queues

@app.on_message(filters.command(["queue", "q", "playlist"]) & filters.group )
async def show_queue(client, message: Message):
    """Show current queue with detailed information"""
    chat_id = message.chat.id
    
    try:
        if chat_id in queues and queues[chat_id]:
            queue_list = queues[chat_id]
            
            # Calculate total duration
            total_duration = sum(track.get('duration', 0) for track in queue_list)
            
            queue_text = f"🎵 **Current Queue ({len(queue_list)} tracks)**\n\n"
            queue_text += f"**Total Duration:** {seconds_to_min(total_duration)}\n\n"
            
            # Show first 10 tracks
            for i, track in enumerate(queue_list[:10], 1):
                title = track.get('title', 'Unknown')
                duration = track.get('duration', 0)
                user = track.get('user', 'Unknown')
                
                # Truncate long titles
                if len(title) > 30:
                    title = title[:27] + "..."
                
                queue_text += f"**{i}.** {title}\n"
                queue_text += f"    ⏱️ {seconds_to_min(duration)} | 👤 {user}\n\n"
            
            if len(queue_list) > 10:
                queue_text += f"**... and {len(queue_list) - 10} more tracks**\n\n"
            
            # Add queue management buttons
            buttons = [
                [
                    InlineKeyboardButton("🔀 Shuffle", callback_data=f"queue_shuffle_{chat_id}"),
                    InlineKeyboardButton("🗑️ Clear", callback_data=f"queue_clear_{chat_id}")
                ],
                [
                    InlineKeyboardButton("📋 Full List", callback_data=f"queue_full_{chat_id}"),
                    InlineKeyboardButton("❌ Close", callback_data="close")
                ]
            ]
            
            await message.reply_text(
                queue_text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await message.reply_text(
                "📭 **Queue is empty**\n\n"
                "Use `/play <song name>` to add songs to the queue.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎵 Play Music", switch_inline_query_current_chat="")]
                ])
            )
    
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_callback_query(filters.regex(r"queue_shuffle_(.*)"))
async def shuffle_queue_callback(client, callback_query: CallbackQuery):
    """Handle shuffle queue callback"""
    chat_id = int(callback_query.data.split("_")[2])
    
    try:
        if chat_id in queues and queues[chat_id]:
            import random
            random.shuffle(queues[chat_id])
            
            await callback_query.answer("🔀 Queue shuffled!", show_alert=False)
            
            # Update the message
            await show_queue_callback(client, callback_query, chat_id)
        else:
            await callback_query.answer("📭 Queue is empty!", show_alert=True)
    
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex(r"queue_clear_(.*)"))
async def clear_queue_callback(client, callback_query: CallbackQuery):
    """Handle clear queue callback"""
    chat_id = int(callback_query.data.split("_")[2])
    
    try:
        if chat_id in queues:
            queue_count = len(queues[chat_id])
            queues[chat_id].clear()
            
            await callback_query.answer(f"🗑️ Cleared {queue_count} tracks!", show_alert=True)
            
            # Update the message
            await callback_query.message.edit_text(
                "📭 **Queue cleared!**\n\n"
                "Use `/play <song name>` to add songs to the queue."
            )
        else:
            await callback_query.answer("📭 Queue is already empty!", show_alert=True)
    
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex(r"queue_full_(.*)"))
async def full_queue_callback(client, callback_query: CallbackQuery):
    """Show full queue list"""
    chat_id = int(callback_query.data.split("_")[2])
    
    try:
        if chat_id in queues and queues[chat_id]:
            queue_list = queues[chat_id]
            
            # Create full queue text
            full_text = f"📋 **Complete Queue ({len(queue_list)} tracks)**\n\n"
            
            for i, track in enumerate(queue_list, 1):
                title = track.get('title', 'Unknown')
                duration = track.get('duration', 0)
                user = track.get('user', 'Unknown')
                
                # Truncate very long titles
                if len(title) > 40:
                    title = title[:37] + "..."
                
                full_text += f"**{i}.** {title}\n"
                full_text += f"    ⏱️ {seconds_to_min(duration)} | 👤 {user}\n\n"
                
                # Limit to prevent message being too long
                if len(full_text) > 3500:
                    remaining = len(queue_list) - i
                    full_text += f"**... and {remaining} more tracks**"
                    break
            
            # Use pastebin for very long queues
            if len(full_text) > 4000:
                from JhoomMusic.utils.pastebin import paste
                paste_url = await paste(full_text, f"Queue for Chat {chat_id}")
                
                if paste_url:
                    await callback_query.message.edit_text(
                        f"📋 **Complete Queue ({len(queue_list)} tracks)**\n\n"
                        f"**Queue is too long, uploaded to:** {paste_url}",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("📋 View Full Queue", url=paste_url)],
                            [InlineKeyboardButton("🔙 Back", callback_data=f"queue_back_{chat_id}")]
                        ])
                    )
                else:
                    await callback_query.answer("❌ Failed to upload queue!", show_alert=True)
            else:
                await callback_query.message.edit_text(
                    full_text,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Back", callback_data=f"queue_back_{chat_id}")]
                    ])
                )
        else:
            await callback_query.answer("📭 Queue is empty!", show_alert=True)
    
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex(r"queue_back_(.*)"))
async def queue_back_callback(client, callback_query: CallbackQuery):
    """Go back to main queue view"""
    chat_id = int(callback_query.data.split("_")[2])
    await show_queue_callback(client, callback_query, chat_id)

async def show_queue_callback(client, callback_query: CallbackQuery, chat_id: int):
    """Helper function to show queue in callback"""
    try:
        if chat_id in queues and queues[chat_id]:
            queue_list = queues[chat_id]
            
            # Calculate total duration
            total_duration = sum(track.get('duration', 0) for track in queue_list)
            
            queue_text = f"🎵 **Current Queue ({len(queue_list)} tracks)**\n\n"
            queue_text += f"**Total Duration:** {seconds_to_min(total_duration)}\n\n"
            
            # Show first 10 tracks
            for i, track in enumerate(queue_list[:10], 1):
                title = track.get('title', 'Unknown')
                duration = track.get('duration', 0)
                user = track.get('user', 'Unknown')
                
                # Truncate long titles
                if len(title) > 30:
                    title = title[:27] + "..."
                
                queue_text += f"**{i}.** {title}\n"
                queue_text += f"    ⏱️ {seconds_to_min(duration)} | 👤 {user}\n\n"
            
            if len(queue_list) > 10:
                queue_text += f"**... and {len(queue_list) - 10} more tracks**\n\n"
            
            # Add queue management buttons
            buttons = [
                [
                    InlineKeyboardButton("🔀 Shuffle", callback_data=f"queue_shuffle_{chat_id}"),
                    InlineKeyboardButton("🗑️ Clear", callback_data=f"queue_clear_{chat_id}")
                ],
                [
                    InlineKeyboardButton("📋 Full List", callback_data=f"queue_full_{chat_id}"),
                    InlineKeyboardButton("❌ Close", callback_data="close")
                ]
            ]
            
            await callback_query.message.edit_text(
                queue_text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await callback_query.message.edit_text(
                "📭 **Queue is empty**\n\n"
                "Use `/play <song name>` to add songs to the queue."
            )
    
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@app.on_message(filters.command(["remove", "rm"]) & filters.group )
@AdminRightsCheck
async def remove_from_queue(client, message: Message, _, chat_id):
    """Remove specific track from queue"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/remove <position>`\n\n"
            "**Example:** `/remove 3` - Remove 3rd track from queue"
        )
    
    try:
        position = int(message.command[1]) - 1  # Convert to 0-based index
        
        if chat_id in queues and queues[chat_id]:
            if 0 <= position < len(queues[chat_id]):
                removed_track = queues[chat_id].pop(position)
                
                await message.reply_text(
                    f"🗑️ **Removed from queue:**\n\n"
                    f"**Track:** {removed_track.get('title', 'Unknown')}\n"
                    f"**Position:** {position + 1}\n"
                    f"**Remaining:** {len(queues[chat_id])} tracks"
                )
            else:
                await message.reply_text(
                    f"❌ **Invalid position!**\n\n"
                    f"Queue has {len(queues[chat_id])} tracks. "
                    f"Use position 1-{len(queues[chat_id])}"
                )
        else:
            await message.reply_text("📭 **Queue is empty!**")
    
    except ValueError:
        await message.reply_text("❌ **Please provide a valid number!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command(["move", "mv"]) & filters.group )
@AdminRightsCheck
async def move_in_queue(client, message: Message, _, chat_id):
    """Move track to different position in queue"""
    
    if len(message.command) < 3:
        return await message.reply_text(
            "**Usage:** `/move <from> <to>`\n\n"
            "**Example:** `/move 5 1` - Move 5th track to 1st position"
        )
    
    try:
        from_pos = int(message.command[1]) - 1  # Convert to 0-based
        to_pos = int(message.command[2]) - 1    # Convert to 0-based
        
        if chat_id in queues and queues[chat_id]:
            queue_length = len(queues[chat_id])
            
            if 0 <= from_pos < queue_length and 0 <= to_pos < queue_length:
                # Move the track
                track = queues[chat_id].pop(from_pos)
                queues[chat_id].insert(to_pos, track)
                
                await message.reply_text(
                    f"🔄 **Track moved!**\n\n"
                    f"**Track:** {track.get('title', 'Unknown')}\n"
                    f"**From position:** {from_pos + 1}\n"
                    f"**To position:** {to_pos + 1}"
                )
            else:
                await message.reply_text(
                    f"❌ **Invalid positions!**\n\n"
                    f"Queue has {queue_length} tracks. "
                    f"Use positions 1-{queue_length}"
                )
        else:
            await message.reply_text("📭 **Queue is empty!**")
    
    except ValueError:
        await message.reply_text("❌ **Please provide valid numbers!**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")