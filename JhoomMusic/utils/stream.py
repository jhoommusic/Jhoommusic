"""
Stream utilities - YouTube search & stream URL extraction
"""

import re
import asyncio
from typing import Optional, Dict, Union, List

import yt_dlp
from youtubesearchpython import VideosSearch

from JhoomMusic.logging import LOGGER


def is_youtube_url(url: str) -> bool:
    patterns = [
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=",
        r"(?:https?://)?youtu\.be/",
        r"(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=",
    ]
    return any(re.search(p, url) for p in patterns)


def is_spotify_url(url: str) -> bool:
    return "open.spotify.com" in url


def ytsearch(query: str, limit: int = 1) -> Optional[Union[list, list[dict]]]:
    """Search YouTube and return results"""
    try:
        search = VideosSearch(query, limit=limit)
        results = search.result()

        if not results or not results.get("result"):
            return None

        if limit == 1:
            data = results["result"][0]
            duration = data.get("duration")  # usually "MM:SS" string
            return {
                "title": data.get("title", "Unknown"),
                "link": data.get("link"),
                "duration": duration,
                "thumbnail": data["thumbnails"][0]["url"] if data.get("thumbnails") else None,
                "videoid": data.get("id"),
            }
        return results["result"]
    except Exception as e:
        LOGGER(__name__).error(f"ytsearch error: {e}")
        return None


def parse_duration(duration) -> int:
    """Convert duration (seconds int or MM:SS / HH:MM:SS string) to seconds"""
    if duration is None:
        return 0
    if isinstance(duration, (int, float)):
        return int(duration)

    try:
        parts = str(duration).split(":")
        parts = [int(p) for p in parts]
        if len(parts) == 3:
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
        if len(parts) == 2:
            return parts[0] * 60 + parts[1]
        return int(parts[0])
    except Exception:
        return 0


async def stream_from_link(link: str) -> Optional[str]:
    """Extract direct streamable URL from a YouTube link"""
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
        LOGGER(__name__).error(f"stream_from_link error: {e}")
        return None


async def get_track_info(query: str) -> Optional[Dict]:
    """
    Main function used by play commands.
    Returns a clean dict with title, url (streamable), duration (seconds), etc.
    """
    try:
        # Case 1: Direct YouTube URL
        if is_youtube_url(query):
            loop = asyncio.get_event_loop()

            def extract_info():
                with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
                    return ydl.extract_info(query, download=False)

            info = await loop.run_in_executor(None, extract_info)
            stream_url = info.get("url")

            if not stream_url:
                stream_url = await stream_from_link(query)

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

        # Case 2: Spotify link → fallback to YouTube search
        if is_spotify_url(query):
            # Simple fallback: search the whole URL as text
            result = ytsearch(query)
            if not result:
                return None
            stream_url = await stream_from_link(result["link"])
            if not stream_url:
                return None
            return {
                "title": result["title"],
                "url": stream_url,
                "duration": parse_duration(result.get("duration")),
                "thumbnail": result.get("thumbnail"),
                "videoid": result.get("videoid"),
                "original_url": result["link"],
                "source": "spotify→youtube",
            }

        # Case 3: Normal search query
        result = ytsearch(query)
        if not result:
            return None

        stream_url = await stream_from_link(result["link"])
        if not stream_url:
            return None

        return {
            "title": result["title"],
            "url": stream_url,
            "duration": parse_duration(result.get("duration")),
            "thumbnail": result.get("thumbnail"),
            "videoid": result.get("videoid"),
            "original_url": result["link"],
            "source": "youtube",
        }

    except Exception as e:
        LOGGER(__name__).error(f"get_track_info error: {e}")
        return None
