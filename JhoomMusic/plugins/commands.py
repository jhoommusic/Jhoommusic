from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from JhoomMusic import app
from config import BANNED_USERS, BOT_NAME, SUPPORT_CHAT, SUPPORT_CHANNEL

# Exact command categories as per your COMMAND_DETAILS
COMMAND_CATEGORIES = {
    "sultan": {
        "title": "👑 SULTAN COMMANDS",
        "description": "MUSIC PLAYBACK CONTROLS",
        "commands": {
            "/pause": "⏸️ PAUSE CURRENT PLAYING STREAM",
            "/resume": "▶️ RESUME PAUSED STREAM", 
            "/skip": "⏭️ SKIP TO NEXT TRACK IN QUEUE",
            "/stop": "⏹️ CLEAN QUEUE AND END STREAM",
            "/player": "🎛️ GET INTERACTIVE PLAYER PANEL",
            "/end": "🔚 END THE STREAM",
            "/queue": "📋 SHOW QUEUED TRACKS LIST"
        }
    },
    "licence": {
        "title": "🔐 LICENCE COMMANDS",
        "description": "USER AUTHORIZATION SYSTEM",
        "commands": {
            "/auth user_id": "✅ ADD USER TO AUTH LIST",
            "/unauth user_id": "❌ REMOVE USER FROM AUTH LIST",
            "/authusers": "👥 SHOWS LIST OF AUTH USERS"
        }
    },
    "broadcast": {
        "title": "📢 BROADCAST COMMANDS",
        "description": "MESSAGE BROADCASTING SYSTEM",
        "commands": {
            "/broadcast text": "📡 BROADCAST TO ALL CHATS",
            "/broadcast -pin": "📌 PIN BROADCASTED MESSAGES",
            "/broadcast -pinloud": "🔊 PIN WITH NOTIFICATION",
            "/broadcast -user": "👤 BROADCAST TO USERS",
            "/broadcast -assistant": "🤖 BROADCAST FROM ASSISTANT",
            "/broadcast -nobot": "🚫 FORCE BOT TO NOT BROADCAST"
        }
    },
    "bl_chat": {
        "title": "🚫 BL-CHAT COMMANDS", 
        "description": "CHAT BLACKLIST MANAGEMENT",
        "commands": {
            "/blacklistchat chat_id": "🚫 BLACKLIST CHAT",
            "/whitelistchat chat_id": "✅ WHITELIST CHAT",
            "/blacklistedchat": "📋 SHOWS BLACKLISTED CHATS"
        }
    },
    "bl_user": {
        "title": "🚫 BL-USER COMMANDS",
        "description": "USER BLOCKING SYSTEM", 
        "commands": {
            "/block username": "🔒 BLOCK USER FROM BOT",
            "/unblock username": "🔓 UNBLOCK USER",
            "/blockedusers": "📋 SHOWS BLOCKED USERS LIST"
        }
    },
    "ch_play": {
        "title": "📺 CH-PLAY COMMANDS",
        "description": "CHANNEL STREAMING CONTROLS",
        "commands": {
            "/cplay": "🎵 STREAM AUDIO IN CHANNEL",
            "/cvplay": "🎬 STREAM VIDEO IN CHANNEL", 
            "/cplayforce": "⚡ FORCE PLAY NEW TRACK",
            "/channelplay": "📺 CONNECT CHANNEL TO GROUP"
        }
    },
    "g_bans": {
        "title": "🌍 G-BANS COMMANDS",
        "description": "GLOBAL BAN SYSTEM",
        "commands": {
            "/gban user_id": "🚫 GLOBALLY BAN USER",
            "/ungban user_id": "✅ REMOVE GLOBAL BAN", 
            "/gbannedusers": "📋 SHOW GLOBALLY BANNED USERS"
        }
    },
    "spiral": {
        "title": "🌀 SPIRAL COMMANDS",
        "description": "LOOPING CONTROLS",
        "commands": {
            "/loop enable/disable": "🔁 TOGGLE LOOP",
            "/loop 1/2/3": "🔢 SET LOOP COUNT"
        }
    },
    "revamp": {
        "title": "🔧 REVAMP COMMANDS", 
        "description": "MAINTENANCE CONTROLS",
        "commands": {
            "/logs": "📝 GET BOT LOGS",
            "/logger": "📊 TOGGLE ACTIVITY LOGGING",
            "/maintenance": "🛠️ TOGGLE MAINTENANCE MODE"
        }
    },
    "ping": {
        "title": "🏓 PING COMMANDS",
        "description": "BOT STATUS SYSTEM", 
        "commands": {
            "/ping": "🏓 SHOW BOT PING AND STATS",
            "/stats": "📊 SHOW BOT STATISTICS",
            "/uptime": "⏰ SHOW BOT UPTIME"
        }
    },
    "play": {
        "title": "🎵 PLAY COMMANDS",
        "description": "MUSIC PLAYBACK SYSTEM",
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
        "description": "QUEUE MANAGEMENT",
        "commands": {
            "/shuffle": "🔀 SHUFFLE THE QUEUE",
            "/queue": "📋 SHOW SHUFFLED QUEUE"
        }
    },
    "seek": {
        "title": "⏩ SEEK COMMANDS", 
        "description": "PLAYBACK POSITION CONTROL",
        "commands": {
            "/seek time-dur": "⏩ SEEK TO POSITION",
            "/seekback time-dur": "⏪ SEEK BACKWARDS"
        }
    },
    "song": {
        "title": "🎵 SONG COMMANDS",
        "description": "TRACK DOWNLOAD SYSTEM",
        "commands": {
            "/song url/name": "📥 DOWNLOAD TRACK FROM YOUTUBE"
        }
    },
    "speed": {
        "title": "⚡ SPEED COMMANDS",
        "description": "PLAYBACK SPEED CONTROLS", 
        "commands": {
            "/speed": "⚡ ADJUST PLAYBACK SPEED IN GROUP",
            "/cSpeed": "⚡ ADJUST SPEED IN CHANNEL"
        }
    },
    # Additional categories from your list
    "vplay": {
        "title": "🎬 VPLAY COMMANDS",
        "description": "VIDEO STREAMING",
        "commands": {
            "/vplay": "🎬 START VIDEO STREAM",
            "/vplayforce": "⚡ FORCE NEW VIDEO STREAM"
        }
    },
    "troubleshoot": {
        "title": "🔧 TROUBLESHOOT COMMANDS",
        "description": "SELF-REPAIR SYSTEM",
        "commands": {
            "/fixbot": "🔧 REPAIR COMMON ISSUES",
            "/diagnose": "🔍 CHECK BOT HEALTH", 
            "/fixproblem": "🛠️ (ADMIN ONLY) REMOTE REPAIRS"
        }
    },
    "settings": {
        "title": "⚙️ SETTINGS COMMANDS",
        "description": "USER PREFERENCES SYSTEM",
        "commands": {
            "/settings": "⚙️ SHOW SETTINGS PANEL",
            "/settings volume [1-200]": "🔊 SET PLAYBACK VOLUME",
            "/settings quality [low|medium|high]": "🎧 SET STREAM QUALITY", 
            "/settings language [en|hi|etc]": "🌐 SET BOT LANGUAGE",
            "/settings notifications [on|off]": "🔔 TOGGLE NOTIFICATIONS"
        }
    },
    "radio": {
        "title": "📻 RADIO COMMANDS",
        "description": "FM RADIO SYSTEM",
        "commands": {
            "/radio search [query]": "🔍 SEARCH RADIO STATIONS",
            "/radio play [ID]": "▶️ PLAY RADIO STATION",
            "/radio stop": "⏹️ STOP RADIO PLAYBACK",
            "/radio list": "📋 SHOW POPULAR STATIONS"
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

**💡 Note:** Make sure bot has admin permissions for full functionality.
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
        
        # Build command list text exactly as per your format
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

**💡 Note:** Make sure bot has admin permissions for full functionality.
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

**🎵 Essential Commands:**
• `/play <song>` - Play music
• `/pause` - Pause playback
• `/resume` - Resume playback
• `/skip` - Skip current song
• `/stop` - Stop and clear queue

**👑 Admin Commands:**
• `/auth <user>` - Authorize user
• `/mute` - Mute assistant
• `/clearqueue` - Clear queue

**📊 Info Commands:**
• `/ping` - Check bot status
• `/queue` - Show current queue

**Need more commands?** Use `/commands` for full list!
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
            "**Example:** `/search_cmd play`"
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
        result_text = f"**❌ No commands found for '{keyword}'**\n\nTry searching with different keywords."
    
    keyboard = [
        [InlineKeyboardButton("📋 All Commands", callback_data="back_to_commands")]
    ]
    
    await message.reply_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )