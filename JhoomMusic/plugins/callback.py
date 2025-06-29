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
    """Show commands interface exactly like the image"""
    
    welcome_text = f"""
**COMMANDS OF JHOOMMUSIC BOT**

**THERE ARE DIFFERENT TYPES OF COMMAND OF JHOOMMUSIC SOME OF THEM ARE ONLY FOR ADMINS AND SOME OF THEM ARE FOR ELITEUSERS.**

**🔧 HOW TO USE COMMANDS?**
├ **TAP ON BUTTON BELOW TO KNOW MORE.**
├ **CHECK FEATURES LIKE ELITEUSERS ETC.**
└ **/:- USE ALL FEATURES WITH THIS HANDLER.**
"""
    
    # Create the exact button layout from the image with SULTAN and LICENCE
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