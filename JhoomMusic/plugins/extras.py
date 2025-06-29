from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from JhoomMusic import app
from config import BANNED_USERS, BOT_NAME

@app.on_message(filters.command(["lyrics", "lyric"]) & ~BANNED_USERS)
async def get_lyrics(client, message: Message):
    """Get song lyrics"""
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/lyrics <song name>`\n\n"
            "**Example:** `/lyrics Imagine Dragons Believer`"
        )
    
    query = " ".join(message.command[1:])
    await message.reply_text(
        f"🔍 **Searching lyrics for:** {query}\n\n"
        "⚠️ **This feature is under development!**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )

@app.on_message(filters.command(["search"]) & ~BANNED_USERS)
async def search_songs(client, message: Message):
    """Search for songs"""
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/search <song name>`\n\n"
            "**Example:** `/search Imagine Dragons`"
        )
    
    query = " ".join(message.command[1:])
    await message.reply_text(
        f"🔍 **Searching for:** {query}\n\n"
        "⚠️ **This feature is under development!**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )

@app.on_message(filters.command(["download", "dl"]) & ~BANNED_USERS)
async def download_song(client, message: Message):
    """Download audio file"""
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/download <song name or link>`\n\n"
            "**Example:** `/download Imagine Dragons Believer`"
        )
    
    query = " ".join(message.command[1:])
    await message.reply_text(
        f"📥 **Downloading:** {query}\n\n"
        "⚠️ **This feature is under development!**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )

@app.on_message(filters.command(["radio"]) & ~BANNED_USERS)
async def play_radio(client, message: Message):
    """Play radio stations"""
    radio_text = """
📻 **RADIO STATIONS**

**Popular Stations:**
• `/radio bollywood` - Bollywood Hits
• `/radio english` - English Pop
• `/radio classical` - Classical Music
• `/radio jazz` - Jazz Radio
• `/radio rock` - Rock Station

⚠️ **This feature is under development!**
"""
    
    await message.reply_text(
        radio_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )

@app.on_message(filters.command(["playlist", "pl"]) & ~BANNED_USERS)
async def manage_playlist(client, message: Message):
    """Manage playlists"""
    playlist_text = """
📋 **PLAYLIST MANAGEMENT**

**Commands:**
• `/playlist create <name>` - Create playlist
• `/playlist add <song>` - Add to playlist
• `/playlist remove <song>` - Remove from playlist
• `/playlist show` - Show all playlists
• `/playlist play <name>` - Play playlist

⚠️ **This feature is under development!**
"""
    
    await message.reply_text(
        playlist_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )

@app.on_message(filters.command(["favorites", "fav"]) & ~BANNED_USERS)
async def manage_favorites(client, message: Message):
    """Manage favorite songs"""
    favorites_text = """
❤️ **FAVORITE SONGS**

**Commands:**
• `/fav add` - Add current song to favorites
• `/fav remove <song>` - Remove from favorites
• `/fav show` - Show favorite songs
• `/fav play` - Play random favorite

⚠️ **This feature is under development!**
"""
    
    await message.reply_text(
        favorites_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )

@app.on_message(filters.command(["history"]) & ~BANNED_USERS)
async def show_history(client, message: Message):
    """Show play history"""
    history_text = """
📚 **PLAY HISTORY**

**Recent Tracks:**
• No tracks played yet

**Commands:**
• `/history` - Show recent tracks
• `/history clear` - Clear history

⚠️ **This feature is under development!**
"""
    
    await message.reply_text(
        history_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )

@app.on_message(filters.command(["nowplaying", "np"]) & ~BANNED_USERS)
async def now_playing(client, message: Message):
    """Show current track info"""
    chat_id = message.chat.id
    
    # Import active_chats from call.py
    from JhoomMusic.core.call import active_chats
    
    if chat_id in active_chats:
        np_text = f"""
🎵 **NOW PLAYING**

**Track:** Currently Playing
**Duration:** Unknown
**Requested by:** User

**Controls:**
• `/pause` - Pause playback
• `/skip` - Skip track
• `/stop` - Stop playback
"""
    else:
        np_text = "❌ **Nothing is currently playing**"
    
    await message.reply_text(
        np_text,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}"),
                InlineKeyboardButton("⏭️ Skip", callback_data=f"skip_{chat_id}")
            ],
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )

@app.on_message(filters.command(["seek"]) & ~BANNED_USERS)
async def seek_track(client, message: Message):
    """Seek to position in track"""
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/seek <time>`\n\n"
            "**Examples:**\n"
            "• `/seek 1:30` - Seek to 1 minute 30 seconds\n"
            "• `/seek 45` - Seek to 45 seconds"
        )
    
    time_str = message.command[1]
    await message.reply_text(
        f"⏩ **Seeking to:** {time_str}\n\n"
        "⚠️ **This feature is under development!**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )

@app.on_message(filters.command(["speed"]) & ~BANNED_USERS)
async def adjust_speed(client, message: Message):
    """Adjust playback speed"""
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/speed <rate>`\n\n"
            "**Examples:**\n"
            "• `/speed 1.5` - 1.5x speed\n"
            "• `/speed 0.75` - 0.75x speed\n"
            "• `/speed 1` - Normal speed"
        )
    
    speed = message.command[1]
    await message.reply_text(
        f"🏃 **Setting speed to:** {speed}x\n\n"
        "⚠️ **This feature is under development!**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Commands", callback_data="back_to_commands")]
        ])
    )