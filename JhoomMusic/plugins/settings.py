from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from JhoomMusic import app
from JhoomMusic.utils.decorators import AdminRightsCheck
from JhoomMusic.utils.database.settings import *
from JhoomMusic.utils.database.language import get_lang, set_lang, get_languages
from JhoomMusic.utils.inline import settings_panel, quality_panel, language_panel
from config import BANNED_USERS

@app.on_message(filters.command(["settings"]) & filters.group)
@AdminRightsCheck
async def settings_command(client, message: Message, _, chat_id):
    """Show settings panel"""
    
    # Get current settings
    playmode = await get_playmode(chat_id)
    playtype = await get_playtype(chat_id)
    quality = await get_quality(chat_id)
    volume = await get_volume(chat_id)
    language = await get_lang(chat_id)
    
    settings_text = f"""
⚙️ **Group Settings**

**🎵 Current Configuration:**
• **Play Mode:** {playmode}
• **Play Type:** {playtype}
• **Audio Quality:** {quality}
• **Volume:** {volume}%
• **Language:** {language.upper()}

**📝 Tap buttons below to modify settings**
"""
    
    await message.reply_text(
        settings_text,
        reply_markup=settings_panel()
    )

@app.on_callback_query(filters.regex("settings_cb"))
async def settings_callback(client, callback_query: CallbackQuery):
    """Handle settings callback"""
    chat_id = callback_query.message.chat.id
    
    # Get current settings
    playmode = await get_playmode(chat_id)
    playtype = await get_playtype(chat_id)
    quality = await get_quality(chat_id)
    volume = await get_volume(chat_id)
    language = await get_lang(chat_id)
    
    settings_text = f"""
⚙️ **Group Settings**

**🎵 Current Configuration:**
• **Play Mode:** {playmode}
• **Play Type:** {playtype}
• **Audio Quality:** {quality}
• **Volume:** {volume}%
• **Language:** {language.upper()}

**📝 Tap buttons below to modify settings**
"""
    
    await callback_query.message.edit_text(
        settings_text,
        reply_markup=settings_panel()
    )

@app.on_callback_query(filters.regex("quality_cb"))
async def quality_callback(client, callback_query: CallbackQuery):
    """Handle quality callback"""
    
    quality_text = """
🎵 **Audio Quality Settings**

**Choose your preferred audio quality:**

• **🔈 Low** - 64kbps (Data Saver)
• **🔉 Medium** - 128kbps (Balanced)
• **🔊 High** - 320kbps (Best Quality)

**Note:** Higher quality uses more bandwidth
"""
    
    await callback_query.message.edit_text(
        quality_text,
        reply_markup=quality_panel()
    )

@app.on_callback_query(filters.regex(r"quality_(.+)"))
async def set_quality_callback(client, callback_query: CallbackQuery):
    """Handle quality selection"""
    quality = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id
    
    quality_map = {
        "low": "Low",
        "medium": "Medium", 
        "high": "High"
    }
    
    await set_quality(chat_id, quality_map[quality])
    
    await callback_query.answer(
        f"✅ Audio quality set to {quality_map[quality]}!",
        show_alert=True
    )
    
    # Go back to settings
    await settings_callback(client, callback_query)

@app.on_callback_query(filters.regex("language_cb"))
async def language_callback(client, callback_query: CallbackQuery):
    """Handle language callback"""
    
    languages = await get_languages()
    lang_text = "🌐 **Language Settings**\n\n**Choose your preferred language:**\n\n"
    
    for code, name in languages.items():
        lang_text += f"• {name}\n"
    
    await callback_query.message.edit_text(
        lang_text,
        reply_markup=language_panel()
    )

@app.on_callback_query(filters.regex(r"lang_(.+)"))
async def set_language_callback(client, callback_query: CallbackQuery):
    """Handle language selection"""
    lang_code = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id
    
    languages = await get_languages()
    
    if lang_code in languages:
        await set_lang(chat_id, lang_code)
        
        await callback_query.answer(
            f"✅ Language set to {languages[lang_code]}!",
            show_alert=True
        )
        
        # Go back to settings
        await settings_callback(client, callback_query)
    else:
        await callback_query.answer("❌ Invalid language!", show_alert=True)

@app.on_callback_query(filters.regex("playmode_cb"))
async def playmode_callback(client, callback_query: CallbackQuery):
    """Handle playmode callback"""
    
    playmode_text = """
🎛️ **Play Mode Settings**

**Choose how music should be played:**

• **Direct** - Play immediately
• **Inline** - Show search results first
• **Queue** - Add to queue automatically

**Current mode will be highlighted**
"""
    
    chat_id = callback_query.message.chat.id
    current_mode = await get_playmode(chat_id)
    
    buttons = []
    modes = ["Direct", "Inline", "Queue"]
    
    for mode in modes:
        text = f"{'✅' if mode == current_mode else '⚪'} {mode}"
        buttons.append([InlineKeyboardButton(text, callback_data=f"setmode_{mode.lower()}")])
    
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="settings_cb")])
    
    await callback_query.message.edit_text(
        playmode_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(r"setmode_(.+)"))
async def set_playmode_callback(client, callback_query: CallbackQuery):
    """Handle playmode selection"""
    mode = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id
    
    mode_map = {
        "direct": "Direct",
        "inline": "Inline",
        "queue": "Queue"
    }
    
    if mode in mode_map:
        await set_playmode(chat_id, mode_map[mode])
        
        await callback_query.answer(
            f"✅ Play mode set to {mode_map[mode]}!",
            show_alert=True
        )
        
        # Refresh playmode panel
        await playmode_callback(client, callback_query)
    else:
        await callback_query.answer("❌ Invalid mode!", show_alert=True)

@app.on_callback_query(filters.regex("volume_cb"))
async def volume_callback(client, callback_query: CallbackQuery):
    """Handle volume callback"""
    
    volume_text = """
🔊 **Volume Settings**

**Adjust playback volume:**

Use the buttons below to set volume level
**Current volume will be shown**
"""
    
    chat_id = callback_query.message.chat.id
    current_volume = await get_volume(chat_id)
    
    buttons = [
        [
            InlineKeyboardButton("🔇 0%", callback_data="vol_0"),
            InlineKeyboardButton("🔈 25%", callback_data="vol_25"),
            InlineKeyboardButton("🔉 50%", callback_data="vol_50")
        ],
        [
            InlineKeyboardButton("🔊 75%", callback_data="vol_75"),
            InlineKeyboardButton("📢 100%", callback_data="vol_100"),
            InlineKeyboardButton("🎚️ Custom", callback_data="vol_custom")
        ],
        [
            InlineKeyboardButton(f"Current: {current_volume}%", callback_data="vol_current")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="settings_cb")
        ]
    ]
    
    await callback_query.message.edit_text(
        volume_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(r"vol_(\d+)"))
async def set_volume_callback(client, callback_query: CallbackQuery):
    """Handle volume selection"""
    volume = int(callback_query.data.split("_")[1])
    chat_id = callback_query.message.chat.id
    
    await set_volume(chat_id, volume)
    
    await callback_query.answer(
        f"✅ Volume set to {volume}%!",
        show_alert=True
    )
    
    # Refresh volume panel
    await volume_callback(client, callback_query)

@app.on_callback_query(filters.regex("vol_current"))
async def current_volume_callback(client, callback_query: CallbackQuery):
    """Show current volume"""
    chat_id = callback_query.message.chat.id
    current_volume = await get_volume(chat_id)
    
    await callback_query.answer(
        f"🔊 Current volume: {current_volume}%",
        show_alert=True
    )

@app.on_message(filters.command(["settings"]) & filters.group)
@AdminRightsCheck
async def volume_command(client, message: Message, _, chat_id):
    """Handle volume command"""
    
    if len(message.command) == 1:
        # Show current volume
        current_volume = await get_volume(chat_id)
        await message.reply_text(f"🔊 **Current Volume:** {current_volume}%")
        return
    
    try:
        volume = int(message.command[1])
        if 0 <= volume <= 200:
            await set_volume(chat_id, volume)
            await message.reply_text(f"✅ **Volume set to {volume}%**")
        else:
            await message.reply_text("❌ **Volume must be between 0-200%**")
    except ValueError:
        await message.reply_text("❌ **Please provide a valid number**")

@app.on_message(filters.command(["settings"]) & filters.group)
@AdminRightsCheck
async def language_command(client, message: Message, _, chat_id):
    """Handle language command"""
    
    if len(message.command) == 1:
        # Show current language
        current_lang = await get_lang(chat_id)
        languages = await get_languages()
        lang_name = languages.get(current_lang, "Unknown")
        
        await message.reply_text(
            f"🌐 **Current Language:** {lang_name}\n\n"
            f"**Available Languages:**\n" + 
            "\n".join([f"• `{code}` - {name}" for code, name in languages.items()]) +
            f"\n\n**Usage:** `/language <code>`"
        )
        return
    
    lang_code = message.command[1].lower()
    languages = await get_languages()
    
    if lang_code in languages:
        await set_lang(chat_id, lang_code)
        await message.reply_text(f"✅ **Language set to {languages[lang_code]}**")
    else:
        await message.reply_text("❌ **Invalid language code!**")