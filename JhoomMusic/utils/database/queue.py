# Simple in-memory queue storage
# Replace with MongoDB later if needed

queues = {}

def get_queue(chat_id: int):
    return queues.get(chat_id, [])

def add_to_queue(chat_id: int, track: dict):
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].append(track)

def clear_queue(chat_id: int):
    if chat_id in queues:
        queues[chat_id].clear()

def is_queue_empty(chat_id: int) -> bool:
    return not bool(queues.get(chat_id))

def pop_queue(chat_id: int):
    if chat_id in queues and queues[chat_id]:
        return queues[chat_id].pop(0)
    return None
