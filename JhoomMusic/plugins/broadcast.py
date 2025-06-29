from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, ChatAdminRequired

import asyncio
from JhoomMusic import app
from JhoomMusic.misc import SUDOERS
from JhoomMusic.utils.database.chats import get_served_chats, get_served_users
from config import BANNED_USERS

@app.on_message(filters.command(["broadcast", "gcast"]) & SUDOERS & ~BANNED_USERS)
async def broadcast_message(client, message: Message):
    """Broadcast message to all served chats"""
    
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/broadcast <message>` - Broadcast text\n"
            "• `/broadcast` (reply to message) - Broadcast replied message\n\n"
            "**Options:**\n"
            "• `-pin` - Pin the message\n"
            "• `-user` - Send to users only\n"
            "• `-group` - Send to groups only"
        )
    
    # Parse options
    options = {
        'pin': '-pin' in message.text,
        'user_only': '-user' in message.text,
        'group_only': '-group' in message.text
    }
    
    # Get message to broadcast
    if message.reply_to_message:
        broadcast_msg = message.reply_to_message
        text = broadcast_msg.text or broadcast_msg.caption or ""
    else:
        # Remove command and options from text
        text = message.text
        for cmd in ['/broadcast', '/gcast', '-pin', '-user', '-group']:
            text = text.replace(cmd, '')
        text = text.strip()
        broadcast_msg = None
    
    if not text and not broadcast_msg:
        return await message.reply_text("❌ **No message to broadcast!**")
    
    # Get target chats
    if options['user_only']:
        targets = await get_served_users()
        target_type = "users"
    elif options['group_only']:
        targets = await get_served_chats()
        target_type = "groups"
    else:
        users = await get_served_users()
        chats = await get_served_chats()
        targets = users + chats
        target_type = "chats"
    
    if not targets:
        return await message.reply_text(f"❌ **No {target_type} found to broadcast!**")
    
    # Start broadcasting
    mystic = await message.reply_text(
        f"📡 **Broadcasting to {len(targets)} {target_type}...**\n\n"
        f"**Progress:** 0/{len(targets)}"
    )
    
    success = 0
    failed = 0
    blocked = 0
    
    for i, chat_id in enumerate(targets):
        try:
            if broadcast_msg:
                # Forward the message
                if broadcast_msg.text:
                    sent_msg = await app.send_message(chat_id, broadcast_msg.text)
                elif broadcast_msg.photo:
                    sent_msg = await app.send_photo(
                        chat_id, 
                        broadcast_msg.photo.file_id,
                        caption=broadcast_msg.caption
                    )
                elif broadcast_msg.video:
                    sent_msg = await app.send_video(
                        chat_id,
                        broadcast_msg.video.file_id,
                        caption=broadcast_msg.caption
                    )
                elif broadcast_msg.audio:
                    sent_msg = await app.send_audio(
                        chat_id,
                        broadcast_msg.audio.file_id,
                        caption=broadcast_msg.caption
                    )
                elif broadcast_msg.document:
                    sent_msg = await app.send_document(
                        chat_id,
                        broadcast_msg.document.file_id,
                        caption=broadcast_msg.caption
                    )
                else:
                    sent_msg = await app.copy_message(chat_id, message.chat.id, broadcast_msg.id)
            else:
                # Send text message
                sent_msg = await app.send_message(chat_id, text)
            
            # Pin message if requested
            if options['pin'] and chat_id < 0:  # Only for groups
                try:
                    await app.pin_chat_message(chat_id, sent_msg.id)
                except:
                    pass
            
            success += 1
            
        except UserIsBlocked:
            blocked += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            # Retry after flood wait
            try:
                if broadcast_msg:
                    await app.copy_message(chat_id, message.chat.id, broadcast_msg.id)
                else:
                    await app.send_message(chat_id, text)
                success += 1
            except:
                failed += 1
        except Exception as e:
            failed += 1
            print(f"Broadcast error for {chat_id}: {e}")
        
        # Update progress every 10 messages
        if (i + 1) % 10 == 0:
            try:
                await mystic.edit_text(
                    f"📡 **Broadcasting to {len(targets)} {target_type}...**\n\n"
                    f"**Progress:** {i + 1}/{len(targets)}\n"
                    f"**Success:** {success}\n"
                    f"**Failed:** {failed}\n"
                    f"**Blocked:** {blocked}"
                )
            except:
                pass
        
        # Small delay to avoid rate limits
        await asyncio.sleep(0.1)
    
    # Final result
    await mystic.edit_text(
        f"📡 **Broadcast Completed!**\n\n"
        f"**Total {target_type}:** {len(targets)}\n"
        f"**✅ Success:** {success}\n"
        f"**❌ Failed:** {failed}\n"
        f"**🚫 Blocked:** {blocked}\n\n"
        f"**Success Rate:** {(success/len(targets)*100):.1f}%"
    )

@app.on_message(filters.command(["fcast", "fbroadcast"]) & SUDOERS & ~BANNED_USERS)
async def forward_broadcast(client, message: Message):
    """Forward broadcast (preserves original formatting)"""
    
    if not message.reply_to_message:
        return await message.reply_text(
            "**Usage:** Reply to a message with `/fcast` to forward it to all chats"
        )
    
    # Get all served chats
    chats = await get_served_chats()
    users = await get_served_users()
    targets = chats + users
    
    if not targets:
        return await message.reply_text("❌ **No chats found to broadcast!**")
    
    mystic = await message.reply_text(
        f"📤 **Forward Broadcasting to {len(targets)} chats...**"
    )
    
    success = 0
    failed = 0
    
    for i, chat_id in enumerate(targets):
        try:
            await app.forward_messages(
                chat_id,
                message.chat.id,
                message.reply_to_message.id
            )
            success += 1
        except Exception as e:
            failed += 1
            print(f"Forward broadcast error for {chat_id}: {e}")
        
        # Update progress
        if (i + 1) % 20 == 0:
            try:
                await mystic.edit_text(
                    f"📤 **Forward Broadcasting...**\n\n"
                    f"**Progress:** {i + 1}/{len(targets)}\n"
                    f"**Success:** {success}\n"
                    f"**Failed:** {failed}"
                )
            except:
                pass
        
        await asyncio.sleep(0.1)
    
    await mystic.edit_text(
        f"📤 **Forward Broadcast Completed!**\n\n"
        f"**Total:** {len(targets)}\n"
        f"**✅ Success:** {success}\n"
        f"**❌ Failed:** {failed}\n\n"
        f"**Success Rate:** {(success/len(targets)*100):.1f}%"
    )

@app.on_message(filters.command(["stats", "gstats"]) & SUDOERS & ~BANNED_USERS)
async def global_stats(client, message: Message):
    """Show global bot statistics"""
    
    mystic = await message.reply_text("📊 **Getting statistics...**")
    
    try:
        # Get counts
        total_users = len(await get_served_users())
        total_chats = len(await get_served_chats())
        
        # Get system info
        from JhoomMusic.utils.sys import get_system_info, get_readable_time
        import psutil
        
        sys_info = get_system_info()
        
        stats_text = f"""
📊 **Global Bot Statistics**

👥 **Users & Chats:**
• **Total Users:** {total_users:,}
• **Total Groups:** {total_chats:,}
• **Total Served:** {total_users + total_chats:,}

💻 **System Status:**
• **CPU Usage:** {sys_info.get('cpu', {}).get('usage_percent', 0)}%
• **RAM Usage:** {sys_info.get('memory', {}).get('percent', 0)}%
• **Disk Usage:** {sys_info.get('disk', {}).get('percent', 0)}%

⏰ **Uptime:**
• **System:** {get_readable_time(int(sys_info.get('system', {}).get('uptime', 0)))}
• **Bot:** {get_readable_time(int(psutil.Process().create_time()))}

🎵 **Music Stats:**
• **Active Calls:** {len(getattr(app, 'active_calls', {}))}
• **Queued Tracks:** {sum(len(queue) for queue in getattr(app, 'queues', {}).values())}
"""
        
        await mystic.edit_text(stats_text)
        
    except Exception as e:
        await mystic.edit_text(f"❌ **Error getting stats:** {str(e)}")