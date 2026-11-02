# Sudo users helper

from config import OWNER_ID, SUDO_USERS

def get_sudoers():
    return list(set(OWNER_ID + SUDO_USERS))

def add_sudo(user_id: int):
    if user_id not in SUDO_USERS:
        SUDO_USERS.append(user_id)

def remove_sudo(user_id: int):
    if user_id in SUDO_USERS:
        SUDO_USERS.remove(user_id)
