from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_panel():
    """Start panel buttons"""
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ Add me to your Group ➕",
                url=f"https://t.me/JhoomMusicBot?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text="🎵 Commands", callback_data="commands_cb"),
            InlineKeyboardButton(text="ℹ️ About", callback_data="about_cb")
        ],
        [
            InlineKeyboardButton(text="🆘 Support", url="https://t.me/JhoomMusicSupport"),
            InlineKeyboardButton(text="📢 Updates", url="https://t.me/JhoomMusicChannel"),
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def music_panel(chat_id: int):
    """Music control panel"""
    buttons = [
        [
            InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}"),
            InlineKeyboardButton("▶️ Resume", callback_data=f"resume_{chat_id}"),
            InlineKeyboardButton("⏭️ Skip", callback_data=f"skip_{chat_id}")
        ],
        [
            InlineKeyboardButton("⏹️ Stop", callback_data=f"stop_{chat_id}"),
            InlineKeyboardButton("🔄 Queue", callback_data=f"queue_{chat_id}"),
            InlineKeyboardButton("❌ Close", callback_data="close")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def commands_panel():
    """Commands panel with exact layout from image"""
    buttons = [
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
    return InlineKeyboardMarkup(buttons)

def settings_panel():
    """Settings panel buttons"""
    buttons = [
        [
            InlineKeyboardButton("🎵 Audio Quality", callback_data="quality_cb"),
            InlineKeyboardButton("🎬 Video Quality", callback_data="video_quality_cb")
        ],
        [
            InlineKeyboardButton("🔊 Volume", callback_data="volume_cb"),
            InlineKeyboardButton("🌐 Language", callback_data="language_cb")
        ],
        [
            InlineKeyboardButton("⚙️ Playmode", callback_data="playmode_cb"),
            InlineKeyboardButton("👥 Auth Users", callback_data="auth_cb")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def quality_panel():
    """Audio quality selection panel"""
    buttons = [
        [
            InlineKeyboardButton("🔈 Low", callback_data="quality_low"),
            InlineKeyboardButton("🔉 Medium", callback_data="quality_medium"),
            InlineKeyboardButton("🔊 High", callback_data="quality_high")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="settings_cb")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def language_panel():
    """Language selection panel"""
    buttons = [
        [
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton("🇮🇳 Hindi", callback_data="lang_hi")
        ],
        [
            InlineKeyboardButton("🇪🇸 Spanish", callback_data="lang_es"),
            InlineKeyboardButton("🇫🇷 French", callback_data="lang_fr")
        ],
        [
            InlineKeyboardButton("🇩🇪 German", callback_data="lang_de"),
            InlineKeyboardButton("🇷🇺 Russian", callback_data="lang_ru")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="settings_cb")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def close_panel():
    """Close button"""
    buttons = [
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ]
    return InlineKeyboardMarkup(buttons)