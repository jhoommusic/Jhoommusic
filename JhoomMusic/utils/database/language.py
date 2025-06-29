from typing import Dict
from JhoomMusic.utils.database.database import temp_db

langdb = temp_db.language


async def get_lang(chat_id: int) -> str:
    """Get language for chat"""
    mode = await langdb.find_one({"chat_id": chat_id})
    if not mode:
        return "en"
    return mode["language"]


async def set_lang(chat_id: int, language: str):
    """Set language for chat"""
    await langdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"language": language}}, 
        upsert=True
    )


async def get_languages() -> Dict[str, str]:
    """Get available languages"""
    return {
        "en": "🇺🇸 English",
        "hi": "🇮🇳 Hindi", 
        "es": "🇪🇸 Spanish",
        "fr": "🇫🇷 French",
        "de": "🇩🇪 German",
        "ru": "🇷🇺 Russian",
        "ar": "🇸🇦 Arabic",
        "pt": "🇵🇹 Portuguese"
    }