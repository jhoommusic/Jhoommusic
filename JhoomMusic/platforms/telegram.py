"""
Telegram Platform Handler
Telegram pe bheje gaye audio/video files ko handle karta hai.
"""

from typing import Optional, Dict
from pyrogram.types import Message

from JhoomMusic.logging import LOGGER


class Telegram:
    def __init__(self):
        self.name = "Telegram"

    async def track_info(self, message: Message) -> Optional[Dict]:
        """
        Telegram audio/video/document message se track info nikaalta hai.
        """
        try:
            audio = message.audio or message.voice or message.video or message.document

            if not audio:
                return None

            file_id = audio.file_id
            title = getattr(audio, "title", None) or getattr(audio, "file_name", None) or "Telegram Audio"
            duration = getattr(audio, "duration", 0) or 0
            file_name = getattr(audio, "file_name", title)

            return {
                "title": title,
                "url": file_id,  # Pyrogram file_id
                "duration": duration,
                "thumbnail": None,
                "videoid": None,
                "original_url": None,
                "source": "telegram",
                "file_name": file_name,
                "is_telegram": True,
            }

        except Exception as e:
            LOGGER(__name__).error(f"Telegram track_info error: {e}")
            return None
