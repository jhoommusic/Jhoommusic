
# TEMP FIX: Dummy language functions

def get_lang(chat_id: int) -> str:
    return "en"

def set_lang(chat_id: int, lang: str) -> None:
    pass

def get_languages() -> dict:
    return {"en": "English", "hi": "Hindi"}
