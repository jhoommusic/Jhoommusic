from typing import Dict, List, Union
from JhoomMusic.utils.database.database import temp_db

chatsdb = temp_db.chats


async def get_served_chats() -> List[int]:
    """Get all served chats"""
    chats = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats.append(chat["chat_id"])
    return chats


async def get_served_users() -> List[int]:
    """Get all served users"""
    users = []
    async for user in chatsdb.find({"chat_id": {"$gt": 0}}):
        users.append(user["chat_id"])
    return users


async def add_served_chat(chat_id: int):
    """Add chat to served chats"""
    is_served = await chatsdb.find_one({"chat_id": chat_id})
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


async def add_served_user(user_id: int):
    """Add user to served users"""
    is_served = await chatsdb.find_one({"chat_id": user_id})
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": user_id})


async def remove_served_chat(chat_id: int):
    """Remove chat from served chats"""
    return await chatsdb.delete_one({"chat_id": chat_id})


async def blacklist_chat(chat_id: int):
    """Blacklist a chat"""
    await chatsdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"blacklisted": True}}, 
        upsert=True
    )


async def whitelist_chat(chat_id: int):
    """Remove chat from blacklist"""
    await chatsdb.update_one(
        {"chat_id": chat_id}, 
        {"$unset": {"blacklisted": ""}}, 
        upsert=True
    )


async def is_blacklisted_chat(chat_id: int) -> bool:
    """Check if chat is blacklisted"""
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return chat.get("blacklisted", False)