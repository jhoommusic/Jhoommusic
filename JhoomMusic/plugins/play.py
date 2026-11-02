"""
Play commands - /play and /vplay
"""

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from tgcaller.exceptions import NoActiveGroupCall

from JhoomMusic import app
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.formatters import seconds_to_min
from JhoomMusic.utils.stream import get_track_info
from config import BANNED_USERS, DURATION_LIMIT_MIN


def play_buttons(chat_id: int):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}"),
                InlineKeyboardButton("⏭️ Skip", callback_data=f"skip_{chat_id}"),
                InlineKeyboardButton("⏹️ Stop", callback_data=f"stop_{chat_id}"),
            ],
            [
                InlineKeyboardButton("📋 Queue", callback_data=f"queue_{chat_id}"),
                InlineKeyboardButton("❌ Close", callback_data="close"),
            ],
        ]
    )


@app.on_message(
    filters.command(["play", "p"]) & filters.group & ~filters.user(BANNED_USERS)
)
async def play_command(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/play <song name or YouTube link>`\n\n"
            "**Examples:**\n"
            "• `/play Believer Imagine Dragons`\n"
            "• `/play https://youtu.be/dQw4w9WgXcQ`"
        )

    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    user_name = message.from_user.first_name

    mystic = await message.reply_text("🔍 **Searching...**")

    try:
        track = await get_track_info(query)

        if not track:
            return await mystic.edit_text(
                "❌ **No results found.**\nTry a different name or link."
            )

        duration = track.get("duration", 0) or 0

        # Duration limit check
        if duration and duration > (DURATION_LIMIT_MIN * 60):
            return await mystic.edit_text(
                f"❌ **Duration limit exceeded**\n\n"
                f"• Track: `{seconds_to_min(duration)}`\n"
                f"• Limit: `{DURATION_LIMIT_MIN} minutes`"
            )

        await mystic.edit_text("📥 **Processing...**")

        # Already playing? → Add to queue
        if Jhoom.is_active(chat_id):
            track_data = {
                "title": track["title"],
                "file": track["url"],
                "duration": duration,
                "user": user_name,
                "video": False,
            }
            Jhoom.add_to_queue(chat_id, track_data)

            return await mystic.edit_text(
                f"➕ **Added to Queue**\n\n"
                f"**Title:** {track['title']}\n"
                f"**Duration:** {seconds_to_min(duration)}\n"
                f"**Requested by:** {user_name}\n"
                f"**Position:** #{len(Jhoom.get_queue(chat_id))}"
            )

        # Not playing → Start now
        success = await Jhoom.join_call(
            chat_id=chat_id,
            original_chat_id=chat_id,
            link=track["url"],
            video=False,
        )

        if success:
            await mystic.edit_text(
                f"🎵 **Now Playing**\n\n"
                f"**Title:** {track['title']}\n"
                f"**Duration:** {seconds_to_min(duration)}\n"
                f"**Requested by:** {user_name}",
                reply_markup=play_buttons(chat_id),
            )
        else:
            await mystic.edit_text(
                "❌ **Failed to join voice chat**\n\n"
                "Make sure:\n"
                "• Voice chat is **active**\n"
                "• Bot is **admin**\n"
                "• Bot can manage voice chats"
            )

    except NoActiveGroupCall:
        await mystic.edit_text(
            "❌ **No active voice chat**\n\nPlease start a voice chat first."
        )
    except Exception as e:
        await mystic.edit_text(f"❌ **Error:** `{str(e)}`")


@app.on_message(
    filters.command(["vplay", "videoplay"])
    & filters.group
    & ~filters.user(BANNED_USERS)
)
async def video_play_command(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/vplay <video name or YouTube link>`"
        )

    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    user_name = message.from_user.first_name

    mystic = await message.reply_text("🔍 **Searching video...**")

    try:
        track = await get_track_info(query)

        if not track:
            return await mystic.edit_text("❌ **No results found.**")

        await mystic.edit_text("📥 **Processing video...**")

        success = await Jhoom.join_call(
            chat_id=chat_id,
            original_chat_id=chat_id,
            link=track["url"],
            video=True,
        )

        if success:
            await mystic.edit_text(
                f"🎬 **Now Playing Video**\n\n"
                f"**Title:** {track['title']}\n"
                f"**Requested by:** {user_name}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "⏸️ Pause", callback_data=f"pause_{chat_id}"
                            ),
                            InlineKeyboardButton(
                                "⏹️ Stop", callback_data=f"stop_{chat_id}"
                            ),
                        ]
                    ]
                ),
            )
        else:
            await mystic.edit_text("❌ **Failed to start video.**")

    except Exception as e:
        await mystic.edit_text(f"❌ **Error:** `{str(e)}`")


# -------------------- Callbacks --------------------

@app.on_callback_query(filters.regex(r"pause_(\d+)"))
async def pause_callback(_, query):
    chat_id = int(query.data.split("_")[1])
    success = await Jhoom.pause_stream(chat_id)
    if success:
        await query.answer("⏸️ Paused")
        # Optional: update buttons later if needed
    else:
        await query.answer("❌ Failed to pause", show_alert=True)


@app.on_callback_query(filters.regex(r"resume_(\d+)"))
async def resume_callback(_, query):
    chat_id = int(query.data.split("_")[1])
    success = await Jhoom.resume_stream(chat_id)
    if success:
        await query.answer("▶️ Resumed")
    else:
        await query.answer("❌ Failed to resume", show_alert=True)


@app.on_callback_query(filters.regex(r"skip_(\d+)"))
async def skip_callback(_, query):
    chat_id = int(query.data.split("_")[1])

    queue = Jhoom.get_queue(chat_id)
    if queue:
        next_track = queue.pop(0)
        success = await Jhoom.skip_stream(
            chat_id, next_track["file"], next_track.get("video", False)
        )
        if success:
            await query.answer("⏭️ Skipped")
            await query.message.edit_text(
                f"⏭️ **Now Playing**\n\n**Title:** {next_track['title']}"
            )
        else:
            await query.answer("❌ Skip failed", show_alert=True)
    else:
        await Jhoom.stop_stream(chat_id)
        await query.answer("Queue empty • Stopped")
        await query.message.edit_text("⏹️ **Queue finished**")


@app.on_callback_query(filters.regex(r"stop_(\d+)"))
async def stop_callback(_, query):
    chat_id = int(query.data.split("_")[1])
    await Jhoom.stop_stream(chat_id)
    await query.answer("⏹️ Stopped")
    await query.message.edit_text("⏹️ **Stopped & queue cleared**")


@app.on_callback_query(filters.regex(r"queue_(\d+)"))
async def queue_callback(_, query):
    chat_id = int(query.data.split("_")[1])
    queue = Jhoom.get_queue(chat_id)

    if not queue:
        return await query.answer("📭 Queue is empty", show_alert=True)

    text = "📋 **Current Queue:**\n\n"
    for i, track in enumerate(queue[:10], 1):
        text += f"`{i}.` {track['title']}\n"

    if len(queue) > 10:
        text += f"\n...and {len(queue) - 10} more"

    await query.answer(text, show_alert=True)


@app.on_callback_query(filters.regex("^close$"))
async def close_callback(_, query):
    await query.message.delete()
    await query.answer()
