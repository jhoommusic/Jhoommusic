"""
YouTube Platform Handler
"""

import asyncio
from typing import Optional, Dict, Union
import re

import yt_dlp
from youtubesearchpython import VideosSearch

from JhoomMusic.logging import LOGGER


class YouTube:
    def __init__(self):
        self.name = "YouTube"

    def is_valid(self, query: str) -> bool:
        patterns = [
            r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=",
            r"(?:https?://)?youtu\.be/",
            r"(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=",
        ]
        return any(re.search(p, query) for p in patterns)

    def search(self, query: str, limit: int = 1) -> Optional[Union[Dict, list]]:
        try:
            search = VideosSearch(query, limit=limit)
            results = search.result()

            if not results or not results.get("result"):
                return None

            if limit == 1:
                data = results["result"][0]
                return {
                    "title": data.get("title", "Unknown"),
                    "link": data.get("link"),
                    "duration": data.get("duration"),
                    "thumbnail": data["thumbnails"][0]["url"] if data.get("thumbnails") else None,
                    "videoid": data.get("id"),
                    "source": "youtube",
                }
            return results["result"]
        except Exception as e:
            LOGGER(__name__).error(f"YouTube search error: {e}")
            return None

    def parse_duration(self, duration) -> int:
        if duration is None:
            return 0
        if isinstance(duration, (int, float)):
            return int(duration)

        try:
            parts = [int(p) for p in str(duration).split(":")]
            if len(parts) == 3:
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            if len(parts) == 2:
                return parts[0] * 60 + parts[1]
            return int(parts[0])
        except Exception:
            return 0

    async def get_stream(self, link: str) -> Optional[str]:
        """Get direct streamable URL"""
        ytdl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
        }

        try:
            loop = asyncio.get_event_loop()

            def extract():
                with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                    return info.get("url"), info

            url, info = await loop.run_in_executor(None, extract)
            return url
        except Exception as e:
            LOGGER(__name__).error(f"YouTube stream error: {e}")
            return None

    async def track_info(self, query: str) -> Optional[Dict]:
        """Main method - returns clean track info"""
        try:
            # Direct YouTube link
            if self.is_valid(query):
                loop = asyncio.get_event_loop()

                def extract_info():
                    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
                        return ydl.extract_info(query, download=False)

                info = await loop.run_in_executor(None, extract_info)
                stream_url = info.get("url") or await self.get_stream(query)

                if not stream_url:
                    return None

                return {
                    "title": info.get("title", "Unknown"),
                    "url": stream_url,
                    "duration": info.get("duration", 0) or 0,
                    "thumbnail": info.get("thumbnail"),
                    "videoid": info.get("id"),
                    "original_url": query,
                    "source": "youtube",
                }

            # Search query
            result = self.search(query)
            if not result:
                return None

            stream_url = await self.get_stream(result["link"])
            if not stream_url:
                return None

            return {
                "title": result["title"],
                "url": stream_url,
                "duration": self.parse_duration(result.get("duration")),
                "thumbnail": result.get("thumbnail"),
                "videoid": result.get("videoid"),
                "original_url": result["link"],
                "source": "youtube",
            }

        except Exception as e:
            LOGGER(__name__).error(f"YouTube track_info error: {e}")
            return None
