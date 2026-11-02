# Chat settings (in-memory)

chat_settings = {}

def get_settings(chat_id: int):
    return chat_settings.get(chat_id, {
        "playmode": "Direct",
        "language": "en",
        "auth": False,
    })

def set_settings(chat_id: int, key: str, value):
    if chat_id not in chat_settings:
        chat_settings[chat_id] = {}
    chat_settings[chat_id][key] = value
