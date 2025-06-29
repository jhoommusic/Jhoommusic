from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from JhoomMusic import app
from config import BANNED_USERS, BOT_NAME, SUPPORT_CHAT, SUPPORT_CHANNEL

# Complete command categories with all 47 commands from your list
COMMAND_CATEGORIES = {
    "sultan": {
        "title": "👑 SULTAN COMMANDS",
        "description": "OWNER & SUDO USER CONTROLS",
        "commands": {
            "/auth [user_id]": "✅ AUTHORIZE A USER",
            "/unauth [user_id]": "❌ REMOVE USER AUTHORIZATION", 
            "/authusers": "👥 LIST AUTHORIZED USERS",
            "/broadcast [message]": "📡 SEND MESSAGE TO ALL CHATS",
            "/gban [user_id]": "🚫 GLOBALLY BAN A USER",
            "/ungban [user_id]": "✅ REMOVE GLOBAL BAN",
            "/gbannedusers": "📋 LIST GLOBALLY BANNED USERS",
            "/maintenance": "🛠️ TOGGLE MAINTENANCE MODE",
            "/logs": "📝 GET BOT LOGS (SUDO-ONLY)",
            "/restart": "🔄 RESTART THE BOT",
            "/revamp": "🔧 BOT MAINTENANCE CONTROLS"
        }
    },
    "licence": {
        "title": "🔐 LICENCE COMMANDS", 
        "description": "USER AUTHORIZATION SYSTEM",
        "commands": {
            "/auth [user_id]": "✅ AUTHORIZE A USER",
            "/unauth [user_id]": "❌ REMOVE USER AUTHORIZATION",
            "/authusers": "👥 LIST AUTHORIZED USERS",
            "/settings": "⚙️ OPEN SETTINGS MENU",
            "/settings volume [1-200]": "🔊 ADJUST PLAYBACK VOLUME",
            "/settings quality [low/medium/high]": "🎧 CHANGE STREAM QUALITY",
            "/settings language [en/hi/etc]": "🌐 CHANGE BOT LANGUAGE",
            "/settings notifications [on/off]": "🔔 TOGGLE NOTIFICATIONS"
        }
    },
    "broadcast": {
        "title": "📢 BROADCAST COMMANDS",
        "description": "MESSAGE BROADCASTING SYSTEM", 
        "commands": {
            "/broadcast [message]": "📡 SEND MESSAGE TO ALL CHATS",
            "/stats": "📊 SHOW BOT STATISTICS",
            "/uptime": "⏰ SHOW BOT UPTIME",
            "/ping": "🏓 CHECK BOT RESPONSE TIME"
        }
    },
    "bl_chat": {
        "title": "🚫 BL-CHAT COMMANDS",
        "description": "CHAT BLACKLIST MANAGEMENT",
        "commands": {
            "/blacklistchat [chat_id]": "🚫 BLACKLIST A CHAT",
            "/whitelistchat [chat_id]": "✅ WHITELIST A CHAT", 
            "/blacklistedchat": "📋 SHOW BLACKLISTED CHATS"
        }
    },
    "bl_user": {
        "title": "🚫 BL-USER COMMANDS",
        "description": "USER BLACKLIST MANAGEMENT",
        "commands": {
            "/block [username]": "🔒 BLOCK USER FROM BOT",
            "/unblock [username]": "🔓 UNBLOCK USER"
        }
    },
    "ch_play": {
        "title": "📺 CH-PLAY COMMANDS",
        "description": "CHANNEL PLAYBACK CONTROLS",
        "commands": {
            "/cplay [query]": "▶️ PLAY MUSIC IN CONNECTED CHANNEL",
            "/cvplay [query]": "🎬 PLAY VIDEO IN CONNECTED CHANNEL",
            "/cplayforce [query]": "⚡ FORCE PLAY NEW TRACK IN CHANNEL",
            "/channelplay": "📺 CONNECT CHANNEL TO GROUP"
        }
    },
    "g_bans": {
        "title": "🌍 G-BANS COMMANDS",
        "description": "GLOBAL BAN MANAGEMENT SYSTEM",
        "commands": {
            "/gban [user_id]": "🚫 GLOBALLY BAN A USER",
            "/ungban [user_id]": "✅ REMOVE GLOBAL BAN",
            "/gbannedusers": "📋 LIST GLOBALLY BANNED USERS"
        }
    },
    "spiral": {
        "title": "🌀 SPIRAL COMMANDS",
        "description": "LOOP & REPEAT CONTROLS",
        "commands": {
            "/loop [enable/disable/1-10]": "🔁 ENABLE/DISABLE LOOPING (TRACK OR QUEUE)"
        }
    },
    "revamp": {
        "title": "🔧 REVAMP COMMANDS",
        "description": "BOT MAINTENANCE & REPAIR",
        "commands": {
            "/revamp": "🔧 BOT MAINTENANCE CONTROLS",
            "/fixbot": "🔧 REPAIR COMMON ISSUES (ADMIN-ONLY)",
            "/diagnose": "🔍 RUN SYSTEM DIAGNOSTICS (ADMIN-ONLY)",
            "/logger": "📝 TOGGLE ACTIVITY LOGGING",
            "/maintenance": "🛠️ TOGGLE MAINTENANCE MODE"
        }
    },
    "ping": {
        "title": "🏓 PING COMMANDS",
        "description": "BOT STATUS & PERFORMANCE",
        "commands": {
            "/ping": "🏓 CHECK BOT RESPONSE TIME",
            "/uptime": "⏰ SHOW BOT UPTIME",
            "/stats": "📊 SHOW BOT STATISTICS"
        }
    },
    "play": {
        "title": "🎵 PLAY COMMANDS",
        "description": "MUSIC PLAYBACK CONTROLS",
        "commands": {
            "/play [song/URL]": "▶️ PLAY MUSIC FROM YOUTUBE/SPOTIFY OR REPLY TO AUDIO FILE",
            "/vplay [video/URL]": "🎬 PLAY VIDEOS FROM YOUTUBE",
            "/pause": "⏸️ PAUSE CURRENT PLAYBACK",
            "/resume": "▶️ RESUME PAUSED PLAYBACK",
            "/skip": "⏭️ SKIP TO NEXT TRACK IN QUEUE",
            "/stop": "⏹️ STOP PLAYBACK AND CLEAR QUEUE",
            "/player": "🎛️ SHOW INTERACTIVE PLAYER PANEL",
            "/queue": "📋 SHOW CURRENT QUEUE",
            "/playlist": "📋 MANAGE YOUR PLAYLISTS",
            "/radio [search/play/stop/list]": "📻 CONTROL RADIO STREAMING"
        }
    },
    "shuffle": {
        "title": "🔀 SHUFFLE COMMANDS",
        "description": "QUEUE MANAGEMENT CONTROLS",
        "commands": {
            "/shuffle": "🔀 SHUFFLE THE CURRENT QUEUE",
            "/queue": "📋 SHOW CURRENT QUEUE"
        }
    },
    "seek": {
        "title": "⏩ SEEK COMMANDS",
        "description": "PLAYBACK POSITION CONTROLS",
        "commands": {
            "/seek [seconds]": "⏩ SEEK TO POSITION IN TRACK",
            "/seekback [seconds]": "⏪ SEEK BACKWARD IN TRACK"
        }
    },
    "song": {
        "title": "🎵 SONG COMMANDS",
        "description": "SONG DOWNLOAD & INFO",
        "commands": {
            "/song [query/URL]": "📥 DOWNLOAD TRACK FROM YOUTUBE"
        }
    },
    "speed": {
        "title": "⚡ SPEED COMMANDS",
        "description": "PLAYBACK SPEED CONTROLS",
        "commands": {
            "/speed": "⚡ ADJUST PLAYBACK SPEED IN GROUP",
            "/cSpeed": "⚡ ADJUST SPEED IN CHANNEL"
        }
    }
}

@app.on_message(filters.command(["commands", "cmd", "help"]) & ~BANNED_USERS)
async def show_commands(client, message: Message):
    """Show comprehensive command interface exactly like the image"""
    
    welcome_text = f"""
**COMMANDS OF {BOT_NAME.upper()} BOT**

**THERE ARE DIFFERENT TYPES OF COMMAND OF {BOT_NAME.upper()} SOME OF THEM ARE ONLY FOR ADMINS AND SOME OF THEM ARE FOR ELITEUSERS.**

**🔧 HOW TO USE COMMANDS?**
├ **TAP ON BUTTON BELOW TO KNOW MORE.**
├ **CHECK FEATURES LIKE ELITEUSERS ETC.**
└ **/:- USE ALL FEATURES WITH THIS HANDLER.**

**💡 Note:** Some commands have alternative short forms (like `/p` for `/play`). Admin commands require sudo privileges.
"""
    
    # Create the exact button layout with SULTAN and LICENCE
    keyboard = [
        # First row - SULTAN, LICENCE, BROADCAST
        [
            InlineKeyboardButton("SULTAN", callback_data="cmd_sultan"),
            InlineKeyboardButton("LICENCE", callback_data="cmd_licence"),
            InlineKeyboardButton("BROADCAST", callback_data="cmd_broadcast")
        ],
        # Second row - BL-CHAT, BL-USER, CH-PLAY
        [
            InlineKeyboardButton("BL-CHAT", callback_data="cmd_bl_chat"),
            InlineKeyboardButton("BL-USER", callback_data="cmd_bl_user"),
            InlineKeyboardButton("CH-PLAY", callback_data="cmd_ch_play")
        ],
        # Third row - G-BANS, SPIRAL, REVAMP
        [
            InlineKeyboardButton("G-BANS", callback_data="cmd_g_bans"),
            InlineKeyboardButton("SPIRAL", callback_data="cmd_spiral"),
            InlineKeyboardButton("REVAMP", callback_data="cmd_revamp")
        ],
        # Fourth row - PING, PLAY, SHUFFLE
        [
            InlineKeyboardButton("PING", callback_data="cmd_ping"),
            InlineKeyboardButton("PLAY", callback_data="cmd_play"),
            InlineKeyboardButton("SHUFFLE", callback_data="cmd_shuffle")
        ],
        # Fifth row - SEEK, SONG, SPEED
        [
            InlineKeyboardButton("SEEK", callback_data="cmd_seek"),
            InlineKeyboardButton("SONG", callback_data="cmd_song"),
            InlineKeyboardButton("SPEED", callback_data="cmd_speed")
        ],
        # Back button
        [
            InlineKeyboardButton("BACK", callback_data="back_to_main")
        ]
    ]
    
    await message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Callback handlers for each command category
@app.on_callback_query(filters.regex(r"cmd_(.+)"))
async def handle_command_category(client, callback_query: CallbackQuery):
    """Handle command category callbacks"""
    category = callback_query.data.split("_")[1]
    
    if category in COMMAND_CATEGORIES:
        cat_info = COMMAND_CATEGORIES[category]
        
        # Build command list text
        command_text = f"**{cat_info['title']}**\n\n"
        command_text += f"**{cat_info['description']}**\n\n"
        
        for cmd, desc in cat_info['commands'].items():
            command_text += f"**{cmd}** :- {desc}\n"
        
        # Create back button
        keyboard = [
            [InlineKeyboardButton("🔙 BACK TO COMMANDS", callback_data="back_to_commands")],
            [InlineKeyboardButton("🏠 MAIN MENU", callback_data="back_to_main")]
        ]
        
        await callback_query.message.edit_text(
            command_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await callback_query.answer("Category not found!", show_alert=True)

@app.on_callback_query(filters.regex("back_to_commands"))
async def back_to_commands(client, callback_query: CallbackQuery):
    """Go back to main commands interface"""
    
    welcome_text = f"""
**COMMANDS OF {BOT_NAME.upper()} BOT**

**THERE ARE DIFFERENT TYPES OF COMMAND OF {BOT_NAME.upper()} SOME OF THEM ARE ONLY FOR ADMINS AND SOME OF THEM ARE FOR ELITEUSERS.**

**🔧 HOW TO USE COMMANDS?**
├ **TAP ON BUTTON BELOW TO KNOW MORE.**
├ **CHECK FEATURES LIKE ELITEUSERS ETC.**
└ **/:- USE ALL FEATURES WITH THIS HANDLER.**

**💡 Note:** Some commands have alternative short forms (like `/p` for `/play`). Admin commands require sudo privileges.
"""
    
    # Create the exact button layout with SULTAN and LICENCE
    keyboard = [
        # First row - SULTAN, LICENCE, BROADCAST
        [
            InlineKeyboardButton("SULTAN", callback_data="cmd_sultan"),
            InlineKeyboardButton("LICENCE", callback_data="cmd_licence"),
            InlineKeyboardButton("BROADCAST", callback_data="cmd_broadcast")
        ],
        # Second row - BL-CHAT, BL-USER, CH-PLAY
        [
            InlineKeyboardButton("BL-CHAT", callback_data="cmd_bl_chat"),
            InlineKeyboardButton("BL-USER", callback_data="cmd_bl_user"),
            InlineKeyboardButton("CH-PLAY", callback_data="cmd_ch_play")
        ],
        # Third row - G-BANS, SPIRAL, REVAMP
        [
            InlineKeyboardButton("G-BANS", callback_data="cmd_g_bans"),
            InlineKeyboardButton("SPIRAL", callback_data="cmd_spiral"),
            InlineKeyboardButton("REVAMP", callback_data="cmd_revamp")
        ],
        # Fourth row - PING, PLAY, SHUFFLE
        [
            InlineKeyboardButton("PING", callback_data="cmd_ping"),
            InlineKeyboardButton("PLAY", callback_data="cmd_play"),
            InlineKeyboardButton("SHUFFLE", callback_data="cmd_shuffle")
        ],
        # Fifth row - SEEK, SONG, SPEED
        [
            InlineKeyboardButton("SEEK", callback_data="cmd_seek"),
            InlineKeyboardButton("SONG", callback_data="cmd_song"),
            InlineKeyboardButton("SPEED", callback_data="cmd_speed")
        ],
        # Back button
        [
            InlineKeyboardButton("BACK", callback_data="back_to_main")
        ]
    ]
    
    await callback_query.message.edit_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Quick access commands
@app.on_message(filters.command(["quickhelp", "qhelp"]) & ~BANNED_USERS)
async def quick_help(client, message: Message):
    """Show quick help with essential commands"""
    
    quick_text = f"""
**⚡ QUICK HELP - {BOT_NAME}**

**🎵 Essential Music Commands:**
• `/play [song/URL]` - Play music from YouTube/Spotify
• `/vplay [video/URL]` - Play videos from YouTube
• `/pause` - Pause current playback
• `/resume` - Resume paused playback
• `/skip` - Skip to next track in queue
• `/stop` - Stop playback and clear queue
• `/queue` - Show current queue

**🔧 Troubleshooting Commands:**
• `/fixbot` - Repair common issues (admin-only)
• `/diagnose` - Run system diagnostics (admin-only)
• `/ping` - Check bot response time

**⚙️ Settings Commands:**
• `/settings` - Open settings menu
• `/settings volume [1-200]` - Adjust volume
• `/settings quality [low/medium/high]` - Change quality

**Need more commands?** Use `/commands` for complete list!
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📋 All Commands", callback_data="back_to_commands"),
            InlineKeyboardButton("🆘 Support", url=SUPPORT_CHAT)
        ]
    ]
    
    await message.reply_text(
        quick_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Command search functionality
@app.on_message(filters.command(["search_cmd", "findcmd"]) & ~BANNED_USERS)
async def search_command(client, message: Message):
    """Search for specific commands"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/search_cmd <keyword>`\n\n"
            "**Examples:**\n"
            "• `/search_cmd play` - Find play commands\n"
            "• `/search_cmd auth` - Find authorization commands\n"
            "• `/search_cmd ban` - Find ban commands"
        )
    
    keyword = " ".join(message.command[1:]).lower()
    found_commands = []
    
    # Search through all command categories
    for category, cat_info in COMMAND_CATEGORIES.items():
        for cmd, desc in cat_info['commands'].items():
            if keyword in cmd.lower() or keyword in desc.lower():
                found_commands.append(f"**{cmd}** - {desc}")
    
    if found_commands:
        result_text = f"**🔍 Search Results for '{keyword}':**\n\n"
        result_text += "\n".join(found_commands[:10])  # Limit to 10 results
        
        if len(found_commands) > 10:
            result_text += f"\n\n**... and {len(found_commands) - 10} more results**"
    else:
        result_text = f"**❌ No commands found for '{keyword}'**\n\nTry searching with different keywords like:\n• play, pause, skip\n• auth, ban, block\n• settings, volume, quality"
    
    keyboard = [
        [InlineKeyboardButton("📋 All Commands", callback_data="back_to_commands")]
    ]
    
    await message.reply_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Alternative command triggers
@app.on_message(filters.command(["help"]) & ~BANNED_USERS)
async def help_redirect(client, message: Message):
    """Redirect help to commands"""
    await show_commands(client, message)

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
async def start_private(client, message: Message):
    """Handle start in private chat"""
    start_text = f"""
🎵 **Welcome to {BOT_NAME}!**

I'm a powerful music bot that can play high-quality music in your Telegram groups!

**🔥 Features:**
• Play music from YouTube/Spotify
• High quality audio streaming
• Queue management
• Admin controls
• Live stream support
• Video calls support

**📚 Quick Commands:**
• `/play <song name>` - Play a song
• `/commands` - Show all commands
• `/help` - Get help

**💡 How to use:**
1. Add me to your group
2. Make me admin with necessary permissions
3. Use `/play <song name>` to start playing music!
"""
    
    keyboard = [
        [
            InlineKeyboardButton(
                "➕ Add me to your Group ➕",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton("🎵 Commands", callback_data="back_to_commands"),
            InlineKeyboardButton("ℹ️ About", callback_data="about_bot")
        ],
        [
            InlineKeyboardButton("🆘 Support", url=SUPPORT_CHAT),
            InlineKeyboardButton("📢 Updates", url=SUPPORT_CHANNEL),
        ]
    ]
    
    await message.reply_text(start_text, reply_markup=InlineKeyboardMarkup(keyboard))