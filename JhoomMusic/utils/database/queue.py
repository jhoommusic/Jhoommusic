from typing import Dict, List, Union
from JhoomMusic.misc import db

async def put_queue(
    chat_id: int,
    original_chat_id: int,
    file: str,
    title: str,
    duration: int,
    user: str,
    vidid: str,
    user_id: int,
    stream: str,
    forceplay: Union[bool, str] = None,
):
    """Add track to queue"""
    put = {
        "title": title,
        "dur": duration,
        "streamtype": stream,
        "by": user,
        "user_id": user_id,
        "vidid": vidid,
        "seconds": duration,
        "played": 0,
        "file": file,
    }
    
    if chat_id not in db:
        db[chat_id] = []
    
    if forceplay:
        db[chat_id].insert(0, put)
    else:
        db[chat_id].append(put)

async def get_queue(chat_id: int) -> List[Dict]:
    """Get queue for chat"""
    return db.get(chat_id, [])

async def pop_an_item(chat_id: int):
    """Remove and return first item from queue"""
    if chat_id in db and db[chat_id]:
        return db[chat_id].pop(0)
    return None

async def is_empty_queue(chat_id: int) -> bool:
    """Check if queue is empty"""
    return chat_id not in db or len(db[chat_id]) == 0

async def task_done(chat_id: int):
    """Clear queue for chat"""
    if chat_id in db:
        db[chat_id].clear()

async def clear_queue(chat_id: int):
    """Clear queue for chat"""
    if chat_id in db:
        db[chat_id].clear()

async def add_to_queue(chat_id: int, track_info: Dict):
    """Add track to queue"""
    if chat_id not in db:
        db[chat_id] = []
    
    db[chat_id].append(track_info)

async def get_queue_length(chat_id: int) -> int:
    """Get queue length"""
    return len(db.get(chat_id, []))

async def shuffle_queue(chat_id: int):
    """Shuffle queue"""
    import random
    if chat_id in db and db[chat_id]:
        random.shuffle(db[chat_id])

async def remove_from_queue(chat_id: int, position: int):
    """Remove track from specific position"""
    if chat_id in db and 0 <= position < len(db[chat_id]):
        return db[chat_id].pop(position)
    return None