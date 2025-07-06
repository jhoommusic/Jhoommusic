# Fixed: Removed invalid character from first line

# Temporary authuser functions (replace with real DB logic)
def save_authuser(chat_id, user_id):
    pass

def delete_authuser(chat_id, user_id):
    pass

def _get_authuser_names(chat_id):
    return []

def is_nonadmin(chat_id, user_id):
    return False
