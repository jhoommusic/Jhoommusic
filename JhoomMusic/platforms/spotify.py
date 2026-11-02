"""
Spotify Platform Handler
Note: Spotify se direct stream nahi milta, isliye YouTube pe search karke play karte hain.
"""

import re
from typing import Optional, Dict

from JhoomMusic.logging import LOGGER
from .youtube import YouTube


class Spotify:
    def __init__(self):
        self.name = "Spotify"
        self.youtube = YouTube()

    def is_valid(self, query: str) -> bool:
        return "open.spotify.com" in query

    def extract_id(self, url: str) -> Optional[str]:
        patterns = [
            r"open\.spotify\.com/track/([a-zA-Z0-9]+)",
            r"open\.spotify\.com/playlist/([a-zA-Z0-9]+)",
            r"open\.spotify\.com/album/([a-zA-Z0-9]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    async def track_info(self, query: str) -> Optional[Dict]:
        """
        Spotify link aaye to YouTube pe search karke best match return karta hai.
        """
        try:
            if not self.is_valid(query):
                return None

            # Abhi simple fallback: poora URL YouTube pe search
            # Baad mein Spotify API add karke better title nikaal sakte hain
            result = await self.youtube.track_info(query)

            if result:
                result["source"] = "spotify→youtube"

            return result

        except Exception as e:
            LOGGER(__name__).error(f"Spotify track_info error: {e}")
            return None
