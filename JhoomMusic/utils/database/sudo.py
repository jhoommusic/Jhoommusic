from typing import List
from JhoomMusic.utils.database.database import temp_db

sudodb = temp_db.sudo


async def get_sudoers() -> List[int]:
    """Get all sudo users"""
    sudoers = []
    async for user in sudodb.find({}):
        sudoers.append(user["user_id"])
    return sudoers


async def add_sudo(user_id: int):
    """Add sudo user"""
    is_sudo = await sudodb.find_one({"user_id": user_id})
    if is_sudo:
        return
    return await sudodb.insert_one({"user_id": user_id})


async def remove_sudo(user_id: int):
    """Remove sudo user"""
    return await sudodb.delete_one({"user_id": user_id})


async def is_sudo(user_id: int) -> bool:
    """Check if user is sudo"""
    user = await sudodb.find_one({"user_id": user_id})
    return bool(user)