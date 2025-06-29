from typing import Dict
from JhoomMusic.utils.database.database import temp_db

settingsdb = temp_db.settings


async def get_playmode(chat_id: int) -> str:
    """Get playmode for chat"""
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return "Direct"
    return mode.get("playmode", "Direct")


async def set_playmode(chat_id: int, mode: str):
    """Set playmode for chat"""
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"playmode": mode}}, 
        upsert=True
    )


async def get_playtype(chat_id: int) -> str:
    """Get playtype for chat"""
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return "Everyone"
    return mode.get("playtype", "Everyone")


async def set_playtype(chat_id: int, mode: str):
    """Set playtype for chat"""
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"playtype": mode}}, 
        upsert=True
    )


async def get_quality(chat_id: int) -> str:
    """Get audio quality for chat"""
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return "High"
    return mode.get("quality", "High")


async def set_quality(chat_id: int, quality: str):
    """Set audio quality for chat"""
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"quality": quality}}, 
        upsert=True
    )


async def get_volume(chat_id: int) -> int:
    """Get volume for chat"""
    mode = await settingsdb.find_one({"chat_id": chat_id})
    if not mode:
        return 100
    return mode.get("volume", 100)


async def set_volume(chat_id: int, volume: int):
    """Set volume for chat"""
    await settingsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"volume": volume}}, 
        upsert=True
    )