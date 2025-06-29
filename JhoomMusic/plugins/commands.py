from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from JhoomMusic import app
from config import BANNED_USERS, BOT_NAME, SUPPORT_CHAT, SUPPORT_CHANNEL

# Command categories with detailed information
COMMAND_CATEGORIES = {
    "chief": {
        "title": "👑 CHIEF COMMANDS",
        "description": "OWNER & SUDO USER CONTROLS",
        "commands": {
            "/auth": "✅ AUTHORIZE USER TO USE BOT",
            "/unauth": "❌ REMOVE USER AUTHORIZATION", 
            "/authusers": "👥 LIST ALL AUTHORIZED USERS",
            "/broadcast": "📡 SEND MESSAGE TO ALL CHATS",
            "/gban": "🚫 GLOBALLY BAN A USER",
            "/ungban": "✅ REMOVE GLOBAL BAN",
            "/gbannedusers": "📋 LIST GLOBALLY BANNED USERS",
            "/maintenance": "🛠️ TOGGLE MAINTENANCE MODE",
            "/logs": "📝 GET BOT LOGS",
            "/restart": "🔄 RESTART THE BOT"
        }
    },
    "permit": {
        "title": "🔐 PERMIT COMMANDS", 
        "description": "USER PERMISSION MANAGEMENT",
        "commands": {
            "/auth": "✅ ADD USER TO AUTH LIST",
            "/unauth": "❌ REMOVE USER FROM AUTH LIST",
            "/authusers": "👥 SHOW AUTHORIZED USERS LIST",
            "/clearauth": "🗑️ CLEAR ALL AUTH USERS",
            "/settings": "⚙️ MANAGE GROUP SETTINGS",
            "/language": "🌐 CHANGE BOT LANGUAGE",
            "/quality": "🎧 SET AUDIO QUALITY",
            "/volume": "🔊 ADJUST VOLUME LEVEL"
        }
    },
    "broadcast": {
        "title": "📢 BROADCAST COMMANDS",
        "description": "MESSAGE BROADCASTING SYSTEM", 
        "commands": {
            "/broadcast": "📡 BROADCAST TO ALL CHATS",
            "/gcast": "🌍 GLOBAL BROADCAST MESSAGE",
            "/fcast": "⚡ FORWARD BROADCAST MESSAGE",
            "/stats": "📊 SHOW BOT STATISTICS",
            "/users": "👥 GET TOTAL USERS COUNT",
            "/chats": "💬 GET TOTAL CHATS COUNT",
            "/served": "📈 SHOW SERVED STATISTICS"
        }
    },
    "bl_chat": {
        "title": "🚫 BL-CHAT COMMANDS",
        "description": "CHAT BLACKLIST MANAGEMENT",
        "commands": {
            "/blacklistchat": "🚫 BLACKLIST A CHAT",
            "/whitelistchat": "✅ WHITELIST A CHAT", 
            "/blacklistedchats": "📋 LIST BLACKLISTED CHATS",
            "/block": "🔒 BLOCK USER FROM BOT",
            "/unblock": "🔓 UNBLOCK USER",
            "/blockedusers": "📋 LIST BLOCKED USERS"
        }
    },
    "bl_user": {
        "title": "🚫 BL-USER COMMANDS",
        "description": "USER BLACKLIST MANAGEMENT",
        "commands": {
            "/gban": "🚫 GLOBALLY BAN A USER",
            "/ungban": "✅ REMOVE GLOBAL BAN",
            "/gbannedusers": "📋 LIST GLOBALLY BANNED USERS",
            "/block": "🔒 BLOCK USER FROM BOT",
            "/unblock": "🔓 UNBLOCK USER FROM BOT",
            "/blockedusers": "📋 SHOW BLOCKED USERS LIST"
        }
    },
    "ch_play": {
        "title": "📺 CH-PLAY COMMANDS",
        "description": "CHANNEL PLAYBACK CONTROLS",
        "commands": {
            "/cplay": "▶️ PLAY MUSIC IN CHANNEL",
            "/cvplay": "🎬 PLAY VIDEO IN CHANNEL",
            "/cplayforce": "⚡ FORCE PLAY IN CHANNEL",
            "/channelplay": "📺 CONNECT CHANNEL TO GROUP",
            "/cpause": "⏸️ PAUSE CHANNEL PLAYBACK",
            "/cresume": "▶️ RESUME CHANNEL PLAYBACK",
            "/cskip": "⏭️ SKIP CHANNEL TRACK",
            "/cstop": "⏹️ STOP CHANNEL PLAYBACK"
        }
    },
    "g_bans": {
        "title": "🌍 G-BANS COMMANDS",
        "description": "GLOBAL BAN MANAGEMENT SYSTEM",
        "commands": {
            "/gban": "🚫 GLOBALLY BAN A USER",
            "/ungban": "✅ REMOVE GLOBAL BAN",
            "/gbannedusers": "📋 LIST ALL GBANNED USERS",
            "/gbanstats": "📊 GLOBAL BAN STATISTICS",
            "/checkgban": "🔍 CHECK IF USER IS GBANNED"
        }
    },
    "spiral": {
        "title": "🌀 SPIRAL COMMANDS",
        "description": "LOOP & REPEAT CONTROLS",
        "commands": {
            "/loop": "🔁 TOGGLE LOOP MODE",
            "/loop enable": "✅ ENABLE LOOP MODE",
            "/loop disable": "❌ DISABLE LOOP MODE",
            "/loop 1": "🔂 LOOP CURRENT TRACK",
            "/loop queue": "🔁 LOOP ENTIRE QUEUE",
            "/repeat": "🔄 REPEAT CURRENT SONG"
        }
    },
    "revamp": {
        "title": "🔧 REVAMP COMMANDS",
        "description": "BOT MAINTENANCE & REPAIR",
        "commands": {
            "/restart": "🔄 RESTART THE BOT",
            "/update": "⬆️ UPDATE BOT VERSION",
            "/maintenance": "🛠️ TOGGLE MAINTENANCE MODE",
            "/fixbot": "🔧 FIX COMMON ISSUES",
            "/diagnose": "🔍 RUN SYSTEM DIAGNOSTICS",
            "/cleanup": "🧹 CLEAN CACHE FILES"
        }
    },
    "ping": {
        "title": "🏓 PING COMMANDS",
        "description": "BOT STATUS & PERFORMANCE",
        "commands": {
            "/ping": "🏓 CHECK BOT RESPONSE TIME",
            "/uptime": "⏰ SHOW BOT UPTIME",
            "/stats": "📊 SHOW BOT STATISTICS",
            "/sysinfo": "💻 SYSTEM INFORMATION",
            "/speed": "⚡ CHECK CONNECTION SPEED"
        }
    },
    "play": {
        "title": "🎵 PLAY COMMANDS",
        "description": "MUSIC PLAYBACK CONTROLS",
        "commands": {
            "/play": "▶️ PLAY MUSIC FROM YOUTUBE",
            "/vplay": "🎬 PLAY VIDEO STREAM",
            "/pause": "⏸️ PAUSE CURRENT STREAM",
            "/resume": "▶️ RESUME PAUSED STREAM",
            "/skip": "⏭️ SKIP TO NEXT TRACK",
            "/stop": "⏹️ STOP PLAYBACK & CLEAR QUEUE",
            "/player": "🎛️ SHOW PLAYER PANEL",
            "/queue": "📋 SHOW CURRENT QUEUE"
        }
    },
    "shuffle": {
        "title": "🔀 SHUFFLE COMMANDS",
        "description": "QUEUE MANAGEMENT CONTROLS",
        "commands": {
            "/shuffle": "🔀 SHUFFLE CURRENT QUEUE",
            "/queue": "📋 SHOW CURRENT QUEUE",
            "/clearqueue": "🗑️ CLEAR ALL QUEUED TRACKS",
            "/remove": "🗑️ REMOVE TRACK FROM QUEUE",
            "/move": "🔄 MOVE TRACK POSITION",
            "/playlist": "📋 MANAGE PLAYLISTS"
        }
    },
    "seek": {
        "title": "⏩ SEEK COMMANDS",
        "description": "PLAYBACK POSITION CONTROLS",
        "commands": {
            "/seek": "⏩ SEEK TO SPECIFIC TIME",
            "/seekback": "⏪ SEEK BACKWARD IN TRACK",
            "/forward": "⏭️ FORWARD 10 SECONDS",
            "/backward": "⏮️ BACKWARD 10 SECONDS",
            "/restart": "🔄 RESTART CURRENT TRACK"
        }
    },
    "song": {
        "title": "🎵 SONG COMMANDS",
        "description": "SONG DOWNLOAD & INFO",
        "commands": {
            "/song": "📥 DOWNLOAD SONG FROM YOUTUBE",
            "/lyrics": "📝 GET SONG LYRICS",
            "/songinfo": "ℹ️ GET SONG INFORMATION",
            "/search": "🔍 SEARCH FOR SONGS",
            "/trending": "🔥 SHOW TRENDING SONGS"
        }
    },
    "speed": {
        "title": "⚡ SPEED COMMANDS",
        "description": "PLAYBACK SPEED CONTROLS",
        "commands": {
            "/speed": "⚡ ADJUST PLAYBACK SPEED",
            "/speed 0.5": "🐌 SLOW SPEED (0.5x)",
            "/speed 1": "▶️ NORMAL SPEED (1x)",
            "/speed 1.5": "⚡ FAST SPEED (1.5x)",
            "/speed 2": "🚀 VERY FAST (2x)",
            "/cspeed": "📺 CHANNEL SPEED CONTROL"
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
"""
    
    # Create the exact button layout from the image
    keyboard = [
        # First row
        [
            InlineKeyboardButton("CHIEF", callback_data="cmd_chief"),
            InlineKeyboardButton("PERMIT", callback_data="cmd_permit"),
            InlineKeyboardButton("BROADCAST", callback_data="cmd_broadcast")
        ],
        # Second row  
        [
            InlineKeyboardButton("BL-CHAT", callback_data="cmd_bl_chat"),
            InlineKeyboardButton("BL-USER", callback_data="cmd_bl_user"),
            InlineKeyboardButton("CH-PLAY", callback_data="cmd_ch_play")
        ],
        # Third row
        [
            InlineKeyboardButton("G-BANS", callback_data="cmd_g_bans"),
            InlineKeyboardButton("SPIRAL", callback_data="cmd_spiral"),
            InlineKeyboardButton("REVAMP", callback_data="cmd_revamp")
        ],
        # Fourth row
        [
            InlineKeyboardButton("PING", callback_data="cmd_ping"),
            InlineKeyboardButton("PLAY", callback_data="cmd_play"),
            InlineKeyboardButton("SHUFFLE", callback_data="cmd_shuffle")
        ],
        # Fifth row
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
"""
    
    # Create the exact button layout from the image
    keyboard = [
        # First row
        [
            InlineKeyboardButton("CHIEF", callback_data="cmd_chief"),
            InlineKeyboardButton("PERMIT", callback_data="cmd_permit"),
            InlineKeyboardButton("BROADCAST", callback_data="cmd_broadcast")
        ],
        # Second row  
        [
            InlineKeyboardButton("BL-CHAT", callback_data="cmd_bl_chat"),
            InlineKeyboardButton("BL-USER", callback_data="cmd_bl_user"),
            InlineKeyboardButton("CH-PLAY", callback_data="cmd_ch_play")
        ],
        # Third row
        [
            InlineKeyboardButton("G-BANS", callback_data="cmd_g_bans"),
            InlineKeyboardButton("SPIRAL", callback_data="cmd_spiral"),
            InlineKeyboardButton("REVAMP", callback_data="cmd_revamp")
        ],
        # Fourth row
        [
            InlineKeyboardButton("PING", callback_data="cmd_ping"),
            InlineKeyboardButton("PLAY", callback_data="cmd_play"),
            InlineKeyboardButton("SHUFFLE", callback_data="cmd_shuffle")
        ],
        # Fifth row
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

@app.on_callback_query(filters.regex("back_to_main"))
async def back_to_main(client, callback_query: CallbackQuery):
    """Go back to main start interface"""
    
    start_text = f"""
🎵 **Welcome to {BOT_NAME}!**

I'm a powerful music bot that can play high-quality music in your Telegram groups!

**🔥 Features:**
• Play music from YouTube
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
    
    await callback_query.message.edit_text(
        start_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@app.on_callback_query(filters.regex("about_bot"))
async def about_bot(client, callback_query: CallbackQuery):
    """Show bot information"""
    
    about_text = f"""
**🎵 THANKS FOR EXPLORING {BOT_NAME.upper()}**

**IF YOU WANT MORE INFORMATION ABOUT ME THEN CHECK THE BELOW BUTTONS** ⬇️

**▶️ PYROGRAM VERSION = 2.0.106**
**▶️ {BOT_NAME.upper()} VERSION = 2.0**

**🔄 ALSO IF YOU FACE ANY KIND OF PROBLEM THEN VISIT OUR SUPPORT CHAT TO REPORT THAT PROBLEM.**
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🆘 SUPPORT ↗️", url=SUPPORT_CHAT),
            InlineKeyboardButton("📢 UPDATES ↗️", url=SUPPORT_CHANNEL)
        ],
        [
            InlineKeyboardButton("🖥️ SYSTEM-INFO", callback_data="system_info")
        ],
        [
            InlineKeyboardButton("🔙 BACK", callback_data="back_to_main")
        ]
    ]
    
    await callback_query.message.edit_text(
        about_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@app.on_callback_query(filters.regex("system_info"))
async def system_info(client, callback_query: CallbackQuery):
    """Show system information"""
    import psutil
    import platform
    from datetime import datetime
    
    # Get system info
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = psutil.boot_time()
    
    system_text = f"""
**🖥️ SYSTEM INFORMATION**

**💻 System Details:**
• **OS:** `{platform.system()} {platform.release()}`
• **Python:** `{platform.python_version()}`
• **Architecture:** `{platform.machine()}`

**📊 Resource Usage:**
• **CPU Usage:** `{cpu_percent}%`
• **RAM Usage:** `{memory.percent}%`
• **Disk Usage:** `{disk.percent}%`

**💾 Memory Info:**
• **Total RAM:** `{round(memory.total / (1024**3), 2)} GB`
• **Available:** `{round(memory.available / (1024**3), 2)} GB`

**⏰ System Uptime:**
• **Boot Time:** `{datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}`
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="system_info"),
            InlineKeyboardButton("🔙 Back", callback_data="about_bot")
        ]
    ]
    
    await callback_query.message.edit_text(
        system_text,
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