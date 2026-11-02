# Auth / Admin helpers (in-memory for now)

auth_users = {}  # chat_id -> set of user_ids

def save_authuser(chat_id: int, user_id: int):
    if chat_id not in auth_users:
        auth_users[chat_id] = set()
    auth_users[chat_id].add(user_id)

def delete_authuser(chat_id: int, user_id: int):
    if chat_id in auth_users:
        auth_users[chat_id].discard(user_id)

def is_authuser(chat_id: int, user_id: int) -> bool:
    return user_id in auth_users.get(chat_id, set())

def get_authusers(chat_id: int):
    return list(auth_users.get(chat_id, set()))

def is_nonadmin_chat(chat_id: int) -> bool:
    # Placeholder
    return False
