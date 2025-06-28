from typing import Dict, List, Union
from JhoomMusic.utils.database.database import temp_db

queuesdb = temp_db.queue

async def put_queue(
    chat_id,
    original_chat_id,
    file,
    title,
    duration,
    user,
    vidid,
    user_id,
    stream,
    forceplay: Union[bool, str] = None,
):
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
    get = await queuesdb.find_one({"chat_id": chat_id})
    if get:
        queued = get["queue"]
        queued.append(put)
        await queuesdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"queue": queued}},
            upsert=True,
        )
    else:
        queue = []
        queue.append(put)
        await queuesdb.insert_one(
            {
                "chat_id": chat_id,
                "original_chat_id": original_chat_id,
                "queue": queue,
            }
        )


async def get_queue(chat_id) -> Dict[str, List[Dict]]:
    get = await queuesdb.find_one({"chat_id": chat_id})
    if not get:
        return {}
    return get


async def pop_an_item(chat_id):
    get = await queuesdb.find_one({"chat_id": chat_id})
    if not get:
        return 0
    queue_list = get["queue"]
    try:
        popped = queue_list.pop(0)
        await queuesdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"queue": queue_list}},
            upsert=True,
        )
        return popped
    except:
        return 0


async def is_empty_queue(chat_id) -> bool:
    get = await queuesdb.find_one({"chat_id": chat_id})
    if not get:
        return True
    if len(get["queue"]) == 0:
        return True
    return False


async def task_done(chat_id):
    await queuesdb.delete_one({"chat_id": chat_id})


async def clear_queue(chat_id):
    await queuesdb.update_one(
        {"chat_id": chat_id}, {"$set": {"queue": []}}, upsert=True
    )