from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from JhoomMusic import app
from config import BANNED_USERS, BOT_NAME, SUPPORT_CHAT, SUPPORT_CHANNEL

# Command categories with detailed information
COMMAND_CATEGORIES = {
    "music": {
        "title": "🎵 MUSIC COMMANDS",
        "description": "BASIC MUSIC PLAYBACK CONTROLS",
        "commands": {
            "/play": "▶️ PLAY MUSIC FROM YOUTUBE",
            "/pause": "⏸️ PAUSE CURRENT PLAYING STREAM",
            "/resume": "▶️ RESUME PAUSED STREAM",
            "/skip": "⏭️ SKIP TO NEXT TRACK IN QUEUE",
            "/stop": "⏹️ CLEAN QUEUE AND END STREAM",
            "/queue": "📋 SHOW QUEUED TRACKS LIST",
            "/shuffle": "🔀 SHUFFLE THE QUEUE",
            "/loop": "🔁 TOGGLE LOOP MODE",
            "/vplay": "🎬 START VIDEO STREAM"
        }
    },
    "admin": {
        "title": "👑 ADMIN COMMANDS",
        "description": "ADMINISTRATIVE CONTROLS FOR GROUP ADMINS",
        "commands": {
            "/auth": "✅ ADD USER TO AUTH LIST",
            "/unauth": "❌ REMOVE USER FROM AUTH LIST",
            "/authusers": "👥 SHOWS LIST OF AUTH USERS",
            "/mute": "🔇 MUTE THE ASSISTANT",
            "/unmute": "🔊 UNMUTE THE ASSISTANT",
            "/clearqueue": "🗑️ CLEAR ALL QUEUED TRACKS"
        }
    },
    "settings": {
        "title": "⚙️ SETTINGS COMMANDS",
        "description": "USER PREFERENCES SYSTEM",
        "commands": {
            "/settings": "🛠️ SHOW SETTINGS PANEL",
            "/language": "🌐 SET BOT LANGUAGE",
            "/quality": "🎧 SET STREAM QUALITY",
            "/volume": "🔊 ADJUST PLAYBACK VOLUME"
        }
    },
    "info": {
        "title": "📊 INFO COMMANDS",
        "description": "BOT STATUS SYSTEM",
        "commands": {
            "/ping": "🏓 SHOW BOT PING AND STATS",
            "/stats": "📈 SHOW BOT STATISTICS",
            "/uptime": "⏰ SHOW BOT UPTIME"
        }
    },
    "broadcast": {
        "title": "📢 BROADCAST COMMANDS",
        "description": "MESSAGE BROADCASTING SYSTEM",
        "commands": {
            "/broadcast": "📡 BROADCAST TO ALL CHATS",
            "/gcast": "🌍 GLOBAL BROADCAST MESSAGE",
            "/fcast": "⚡ FORWARD BROADCAST MESSAGE"
        }
    },
    "maintenance": {
        "title": "🔧 MAINTENANCE COMMANDS",
        "description": "BOT MAINTENANCE CONTROLS",
        "commands": {
            "/logs": "📝 GET BOT LOGS",
            "/restart": "🔄 RESTART THE BOT",
            "/update": "⬆️ UPDATE BOT VERSION",
            "/maintenance": "🛠️ TOGGLE MAINTENANCE MODE"
        }
    }
}

@app.on_message(filters.command(["commands", "cmd", "help"]) & ~BANNED_USERS)
async def show_commands(client, message: Message):
    """Show comprehensive command interface"""
    
    welcome_text = f"""
**🎵 COMMANDS OF {BOT_NAME.upper()} BOT**

**THERE ARE DIFFERENT TYPES OF COMMANDS. SOME OF THEM ARE ONLY FOR ADMINS AND SOME OF THEM ARE FOR ALL USERS.**

**🔧 HOW TO USE COMMANDS?**
├ **TAP ON BUTTON BELOW TO KNOW MORE.**
├ **CHECK FEATURES LIKE ADMIN CONTROLS ETC.**
└ **/:- USE ALL FEATURES WITH THIS HANDLER.**

**💡 Note:** Make sure bot has admin permissions for full functionality.
"""
    
    # Create main command buttons
    keyboard = []
    
    # First row - Main categories
    keyboard.append([
        InlineKeyboardButton("🎵 MUSIC", callback_data="cmd_music"),
        InlineKeyboardButton("👑 ADMIN", callback_data="cmd_admin"),
        InlineKeyboardButton("📢 BROADCAST", callback_data="cmd_broadcast")
    ])
    
    # Second row - Settings and info
    keyboard.append([
        InlineKeyboardButton("⚙️ SETTINGS", callback_data="cmd_settings"),
        InlineKeyboardButton("📊 INFO", callback_data="cmd_info"),
        InlineKeyboardButton("🔧 MAINTENANCE", callback_data="cmd_maintenance")
    ])
    
    # Third row - Additional features
    keyboard.append([
        InlineKeyboardButton("🎲 EXTRAS", callback_data="cmd_extras"),
        InlineKeyboardButton("🆘 SUPPORT", url=SUPPORT_CHAT),
        InlineKeyboardButton("📢 UPDATES", url=SUPPORT_CHANNEL)
    ])
    
    # Fourth row - Back button
    keyboard.append([
        InlineKeyboardButton("🔙 BACK TO MAIN", callback_data="back_to_main")
    ])
    
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
    
    elif category == "extras":
        # Handle extras category
        extras_text = f"""
**🎲 EXTRA COMMANDS**

**ADDITIONAL FEATURES AND UTILITIES**

**/lyrics** :- 📝 GET SONG LYRICS
**/search** :- 🔍 SEARCH FOR SONGS
**/download** :- 💾 DOWNLOAD AUDIO FILE
**/radio** :- 📻 PLAY RADIO STATIONS
**/playlist** :- 📋 MANAGE PLAYLISTS
**/favorites** :- ❤️ MANAGE FAVORITE SONGS
**/history** :- 📚 VIEW PLAY HISTORY
**/nowplaying** :- 🎵 CURRENT TRACK INFO
**/seek** :- ⏩ SEEK TO POSITION
**/speed** :- 🏃 ADJUST PLAYBACK SPEED
"""
        
        keyboard = [
            [InlineKeyboardButton("🔙 BACK TO COMMANDS", callback_data="back_to_commands")],
            [InlineKeyboardButton("🏠 MAIN MENU", callback_data="back_to_main")]
        ]
        
        await callback_query.message.edit_text(
            extras_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

@app.on_callback_query(filters.regex("back_to_commands"))
async def back_to_commands(client, callback_query: CallbackQuery):
    """Go back to main commands interface"""
    
    welcome_text = f"""
**🎵 COMMANDS OF {BOT_NAME.upper()} BOT**

**THERE ARE DIFFERENT TYPES OF COMMANDS. SOME OF THEM ARE ONLY FOR ADMINS AND SOME OF THEM ARE FOR ALL USERS.**

**🔧 HOW TO USE COMMANDS?**
├ **TAP ON BUTTON BELOW TO KNOW MORE.**
├ **CHECK FEATURES LIKE ADMIN CONTROLS ETC.**
└ **/:- USE ALL FEATURES WITH THIS HANDLER.**

**💡 Note:** Make sure bot has admin permissions for full functionality.
"""
    
    # Create main command buttons
    keyboard = []
    
    # First row - Main categories
    keyboard.append([
        InlineKeyboardButton("🎵 MUSIC", callback_data="cmd_music"),
        InlineKeyboardButton("👑 ADMIN", callback_data="cmd_admin"),
        InlineKeyboardButton("📢 BROADCAST", callback_data="cmd_broadcast")
    ])
    
    # Second row - Settings and info
    keyboard.append([
        InlineKeyboardButton("⚙️ SETTINGS", callback_data="cmd_settings"),
        InlineKeyboardButton("📊 INFO", callback_data="cmd_info"),
        InlineKeyboardButton("🔧 MAINTENANCE", callback_data="cmd_maintenance")
    ])
    
    # Third row - Additional features
    keyboard.append([
        InlineKeyboardButton("🎲 EXTRAS", callback_data="cmd_extras"),
        InlineKeyboardButton("🆘 SUPPORT", url=SUPPORT_CHAT),
        InlineKeyboardButton("📢 UPDATES", url=SUPPORT_CHANNEL)
    ])
    
    # Fourth row - Back button
    keyboard.append([
        InlineKeyboardButton("🔙 BACK TO MAIN", callback_data="back_to_main")
    ])
    
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