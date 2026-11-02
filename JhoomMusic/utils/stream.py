"""
Stream utilities - now powered by platforms system
"""

from typing import Optional, Dict

from JhoomMusic.platforms import get_platform
from JhoomMusic.logging import LOGGER


async def get_track_info(query: str) -> Optional[Dict]:
    """
    Main entry point used by play commands.
    Automatically detects platform and returns track info.
    """
    try:
        platform = await get_platform(query)
        track = await platform.track_info(query)

        if track:
            LOGGER(__name__).info(
                f"Track found via {track.get('source', 'unknown')}: {track.get('title')}"
            )
        return track

    except Exception as e:
        LOGGER(__name__).error(f"get_track_info error: {e}")
        return None
