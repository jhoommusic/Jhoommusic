import os
import re
import yt_dlp
import asyncio
from typing import Union, Optional, Dict, List
from youtubesearchpython import VideosSearch

def ytsearch(query: str, limit: int = 1) -> Union[List, int]:
    """Search YouTube for videos"""
    try:
        search = VideosSearch(query, limit=limit)
        results = search.result()
        
        if not results["result"]:
            return 0
        
        if limit == 1:
            data = results["result"][0]
            return [
                data["title"],
                data["link"],
                data["duration"],
                data["thumbnails"][0]["url"] if data["thumbnails"] else None,
                data["id"]
            ]
        else:
            return results["result"]
    except Exception as e:
        print(f"Error in ytsearch: {e}")
        return 0

async def ytdl(format_id: Union[str, int] = "best"):
    """Create YouTube-DL instance"""
    ytdl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "format": format_id,
    }
    return yt_dlp.YoutubeDL(ytdl_opts)

def get_formats(videoid: str) -> tuple:
    """Get available formats for a video"""
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(
                f"https://youtube.com/watch?v={videoid}", 
                download=False
            )
        
        quality = 720
        format_id = None
        
        # Find best format
        for f in info.get("formats", []):
            if f.get("height") == quality and f.get("ext") == "mp4":
                format_id = f["format_id"]
                break
        
        if not format_id:
            for f in info.get("formats", []):
                if (f.get("height") and 
                    f.get("height") <= quality and 
                    f.get("ext") == "mp4"):
                    format_id = f["format_id"]
                    quality = f["height"]
        
        if not format_id:
            format_id = "best[height<=720]"
        
        return format_id, quality
    except Exception as e:
        print(f"Error getting formats: {e}")
        return "best", 720

async def stream_from_link(link: str) -> Optional[str]:
    """Get stream URL from YouTube link"""
    ytdl_opts = {
        "format": "best[height<=720]/best",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
    }
    
    try:
        loop = asyncio.get_event_loop()
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        
        def extract():
            info = ydl.extract_info(link, download=False)
            return info.get("url")
        
        url = await loop.run_in_executor(None, extract)
        return url
    except Exception as e:
        print(f"Error in stream_from_link: {e}")
        return None

async def download_track(query: str, audio_only: bool = True) -> Optional[Dict]:
    """Download track and return info"""
    try:
        # Search for the track
        search_result = ytsearch(query)
        if search_result == 0:
            return None
        
        title, url, duration, thumbnail, videoid = search_result
        
        # Get stream URL
        stream_url = await stream_from_link(url)
        if not stream_url:
            return None
        
        return {
            "title": title,
            "url": stream_url,
            "duration": duration,
            "thumbnail": thumbnail,
            "videoid": videoid,
            "original_url": url,
            "audio_only": audio_only
        }
    except Exception as e:
        print(f"Error downloading track: {e}")
        return None

def extract_spotify_id(url: str) -> Optional[str]:
    """Extract Spotify track/playlist ID from URL"""
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

def is_youtube_url(url: str) -> bool:
    """Check if URL is a YouTube URL"""
    youtube_patterns = [
        r"youtube\.com/watch\?v=",
        r"youtu\.be/",
        r"youtube\.com/playlist\?list=",
    ]
    
    return any(re.search(pattern, url) for pattern in youtube_patterns)

def is_spotify_url(url: str) -> bool:
    """Check if URL is a Spotify URL"""
    return "open.spotify.com" in url

async def get_track_info(query: str) -> Optional[Dict]:
    """Get track information from various sources"""
    try:
        if is_youtube_url(query):
            # Direct YouTube URL
            stream_url = await stream_from_link(query)
            if stream_url:
                # Extract video info
                with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                    info = ydl.extract_info(query, download=False)
                    return {
                        "title": info.get("title", "Unknown"),
                        "url": stream_url,
                        "duration": info.get("duration", 0),
                        "thumbnail": info.get("thumbnail"),
                        "videoid": info.get("id"),
                        "original_url": query,
                        "source": "youtube"
                    }
        
        elif is_spotify_url(query):
            # Spotify URL - need to search on YouTube
            spotify_id = extract_spotify_id(query)
            if spotify_id:
                # For now, just search the URL as text
                return await download_track(query)
        
        else:
            # Search query
            return await download_track(query)
    
    except Exception as e:
        print(f"Error getting track info: {e}")
        return None