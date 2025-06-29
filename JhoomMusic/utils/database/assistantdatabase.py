from typing import Dict, List, Union
from JhoomMusic.utils.database.database import temp_db

assistantdb = temp_db.assistant


async def get_assistant(chat_id: int) -> Dict:
    """Get assistant info for chat"""
    assistant = await assistantdb.find_one({"chat_id": chat_id})
    if not assistant:
        return {}
    return assistant


async def set_assistant(chat_id: int, assistant_id: int, assistant_name: str):
    """Set assistant for chat"""
    await assistantdb.update_one(
        {"chat_id": chat_id}, 
        {"$set": {"assistant_id": assistant_id, "assistant_name": assistant_name}}, 
        upsert=True
    )


async def delete_assistant(chat_id: int):
    """Remove assistant from chat"""
    await assistantdb.delete_one({"chat_id": chat_id})


async def get_all_assistants() -> List[Dict]:
    """Get all assistants"""
    assistants = []
    async for assistant in assistantdb.find({}):
        assistants.append(assistant)
    return assistants