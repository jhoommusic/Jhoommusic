"""
Platforms package - handles different music sources
"""

from .youtube import YouTube
from .spotify import Spotify
from .telegram import Telegram

# Future:
# from .apple import Apple
# from .resso import Resso
# from .soundcloud import SoundCloud

platforms = {
    "youtube": YouTube,
    "spotify": Spotify,
    "telegram": Telegram,
}


async def get_platform(query: str):
    """
    Detect platform from query and return the right handler.
    """
    query = query.strip()

    if "open.spotify.com" in query:
        return Spotify()
    elif "music.apple.com" in query:
        # return Apple()
        return YouTube()  # fallback for now
    elif "resso.com" in query or "resso.onelink.me" in query:
        return YouTube()
    elif "soundcloud.com" in query:
        return YouTube()
    else:
        # Default to YouTube (search or direct link)
        return YouTube()
