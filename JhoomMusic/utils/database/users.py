from typing import Dict, List
from JhoomMusic.utils.database.database import temp_db

usersdb = temp_db.users


async def get_users_count() -> int:
    """Get total users count"""
    users = usersdb.find({"chat_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)


async def get_chats_count() -> int:
    """Get total chats count"""
    chats = usersdb.find({"chat_id": {"$lt": 0}})
    chats = await chats.to_list(length=100000)
    return len(chats)


async def add_user(user_id: int, user_name: str = "Unknown"):
    """Add user to database"""
    is_user = await usersdb.find_one({"chat_id": user_id})
    if is_user:
        return
    return await usersdb.insert_one({
        "chat_id": user_id,
        "user_name": user_name,
        "type": "user"
    })


async def add_chat(chat_id: int, chat_name: str = "Unknown"):
    """Add chat to database"""
    is_chat = await usersdb.find_one({"chat_id": chat_id})
    if is_chat:
        return
    return await usersdb.insert_one({
        "chat_id": chat_id,
        "chat_name": chat_name,
        "type": "group"
    })


async def get_user_info(user_id: int) -> Dict:
    """Get user information"""
    user = await usersdb.find_one({"chat_id": user_id})
    if not user:
        return {}
    return user


async def update_user_info(user_id: int, user_name: str):
    """Update user information"""
    await usersdb.update_one(
        {"chat_id": user_id},
        {"$set": {"user_name": user_name}},
        upsert=True
    )