from typing import Dict
from JhoomMusic.utils.database.database import temp_db

onoffdb = temp_db.onoff


async def is_on(chat_id: int, feature: str) -> bool:
    """Check if feature is enabled"""
    onoff = await onoffdb.find_one({"chat_id": chat_id})
    if not onoff:
        return True
    return onoff.get(feature, True)


async def set_on(chat_id: int, feature: str):
    """Enable feature"""
    await onoffdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {feature: True}}, 
        upsert=True
    )


async def set_off(chat_id: int, feature: str):
    """Disable feature"""
    await onoffdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {feature: False}}, 
        upsert=True
    )


async def get_settings(chat_id: int) -> Dict:
    """Get all settings for chat"""
    settings = await onoffdb.find_one({"chat_id": chat_id})
    if not settings:
        return {
            "welcome": True,
            "cleanmode": False,
            "suggestion": True,
            "autoend": True
        }
    return settings