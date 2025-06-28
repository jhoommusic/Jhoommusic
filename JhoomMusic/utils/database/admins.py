from typing import Dict, List, Union
from JhoomMusic.utils.database.database import temp_db

admindb = temp_db.adminlist


async def get_admins(chat_id: int) -> Dict[str, List[int]]:
    admins = await admindb.find_one({"chat_id": chat_id})
    if not admins:
        return {}
    return admins["admins"]


async def set_admins(chat_id: int, admins_dict: Dict[str, List[int]]):
    await admindb.update_one(
        {"chat_id": chat_id}, {"$set": {"admins": admins_dict}}, upsert=True
    )


async def delete_admins(chat_id: int):
    await admindb.delete_one({"chat_id": chat_id})