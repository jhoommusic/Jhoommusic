# Assistant related helpers (stub)

active_assistants = {}

def set_assistant(chat_id: int, assistant_id: int):
    active_assistants[chat_id] = assistant_id

def get_assistant(chat_id: int):
    return active_assistants.get(chat_id)

def remove_assistant(chat_id: int):
    if chat_id in active_assistants:
        del active_assistants[chat_id]
