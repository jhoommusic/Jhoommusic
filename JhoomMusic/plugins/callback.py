from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from JhoomMusic import app
from JhoomMusic.utils.inline import start_panel, close_panel

@app.on_callback_query(filters.regex("close"))
async def close_callback(client, callback_query: CallbackQuery):
    """Handle close button"""
    try:
        await callback_query.message.delete()
        await callback_query.answer("❌ Closed!", show_alert=False)
    except:
        await callback_query.answer("❌ Closed!", show_alert=False)

@app.on_callback_query(filters.regex("back_to_main"))
async def back_to_main_callback(client, callback_query: CallbackQuery):
    """Go back to main start interface"""
    
    start_text = f"""
🎵 **Welcome to JhoomMusic!**

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
    
    try:
        await callback_query.message.edit_text(
            start_text,
            reply_markup=start_panel()
        )
    except:
        await callback_query.answer("Error loading main menu", show_alert=True)

@app.on_callback_query(filters.regex("commands_cb"))
async def commands_callback(client, callback_query: CallbackQuery):
    """Show commands interface"""
    
    welcome_text = f"""
**🎵 COMMANDS OF JHOOMMUSIC BOT**

**THERE ARE DIFFERENT TYPES OF COMMANDS. SOME OF THEM ARE ONLY FOR ADMINS AND SOME OF THEM ARE FOR ALL USERS.**

**🔧 HOW TO USE COMMANDS?**
├ **TAP ON BUTTON BELOW TO KNOW MORE.**
├ **CHECK FEATURES LIKE ADMIN CONTROLS ETC.**
└ **/:- USE ALL FEATURES WITH THIS HANDLER.**

**💡 Note:** Make sure bot has admin permissions for full functionality.
"""
    
    # Create main command buttons
    keyboard = [
        [
            InlineKeyboardButton("🎵 MUSIC", callback_data="cmd_music"),
            InlineKeyboardButton("👑 ADMIN", callback_data="cmd_admin"),
            InlineKeyboardButton("📢 BROADCAST", callback_data="cmd_broadcast")
        ],
        [
            InlineKeyboardButton("⚙️ SETTINGS", callback_data="cmd_settings"),
            InlineKeyboardButton("📊 INFO", callback_data="cmd_info"),
            InlineKeyboardButton("🔧 MAINTENANCE", callback_data="cmd_maintenance")
        ],
        [
            InlineKeyboardButton("🎲 EXTRAS", callback_data="cmd_extras"),
            InlineKeyboardButton("🆘 SUPPORT", url="https://t.me/JhoomMusicSupport"),
            InlineKeyboardButton("📢 UPDATES", url="https://t.me/JhoomMusicChannel")
        ],
        [
            InlineKeyboardButton("🔙 BACK TO MAIN", callback_data="back_to_main")
        ]
    ]
    
    try:
        await callback_query.message.edit_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except:
        await callback_query.answer("Error loading commands", show_alert=True)

@app.on_callback_query(filters.regex("about_cb"))
async def about_callback(client, callback_query: CallbackQuery):
    """Show about information"""
    
    about_text = f"""
**🎵 THANKS FOR EXPLORING JHOOMMUSIC**

**IF YOU WANT MORE INFORMATION ABOUT ME THEN CHECK THE BELOW BUTTONS** ⬇️

**▶️ PYROGRAM VERSION = 2.0.106**
**▶️ JHOOMMUSIC VERSION = 2.0**

**🔄 ALSO IF YOU FACE ANY KIND OF PROBLEM THEN VISIT OUR SUPPORT CHAT TO REPORT THAT PROBLEM.**
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🆘 SUPPORT ↗️", url="https://t.me/JhoomMusicSupport"),
            InlineKeyboardButton("📢 UPDATES ↗️", url="https://t.me/JhoomMusicChannel")
        ],
        [
            InlineKeyboardButton("🖥️ SYSTEM-INFO", callback_data="system_info")
        ],
        [
            InlineKeyboardButton("🔙 BACK", callback_data="back_to_main")
        ]
    ]
    
    try:
        await callback_query.message.edit_text(
            about_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except:
        await callback_query.answer("Error loading about", show_alert=True)

@app.on_callback_query(filters.regex("system_info"))
async def system_info_callback(client, callback_query: CallbackQuery):
    """Show system information"""
    
    try:
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
                InlineKeyboardButton("🔙 Back", callback_data="about_cb")
            ]
        ]
        
        await callback_query.message.edit_text(
            system_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

# Command category handlers
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
            "/vplay": "🎬 START VIDEO STREAM",
            "/radio": "📻 PLAY RADIO STATIONS"
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
            "/clearqueue": "🗑️ CLEAR ALL QUEUED TRACKS",
            "/remove": "🗑️ REMOVE TRACK FROM QUEUE",
            "/move": "🔄 MOVE TRACK IN QUEUE"
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
            "/nowplaying": "🎵 CURRENT TRACK INFO"
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
            "/shell": "💻 EXECUTE SHELL COMMANDS"
        }
    },
    "extras": {
        "title": "🎲 EXTRA COMMANDS",
        "description": "ADDITIONAL FEATURES AND UTILITIES",
        "commands": {
            "/lyrics": "📝 GET SONG LYRICS",
            "/songinfo": "ℹ️ GET SONG INFORMATION",
            "/download": "💾 DOWNLOAD AUDIO FILE",
            "/playlist": "📋 MANAGE PLAYLISTS",
            "/favorites": "❤️ MANAGE FAVORITE SONGS"
        }
    }
}

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
            [InlineKeyboardButton("🔙 BACK TO COMMANDS", callback_data="commands_cb")],
            [InlineKeyboardButton("🏠 MAIN MENU", callback_data="back_to_main")]
        ]
        
        try:
            await callback_query.message.edit_text(
                command_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except:
            await callback_query.answer("Error loading commands", show_alert=True)
    else:
        await callback_query.answer("Category not found!", show_alert=True)