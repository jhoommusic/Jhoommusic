import os
import re
import yt_dlp
from typing import Union
from youtubesearchpython import VideosSearch

def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = data["thumbnails"][0]["url"]
        videoid = data["id"]
        return [songname, url, duration, thumbnail, videoid]
    except Exception as e:
        print(f"Error in ytsearch: {e}")
        return 0


async def ytdl(format: Union[str, int]):
    ytdl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
    }
    ydl = yt_dlp.YoutubeDL(ytdl_opts)
    return ydl


def get_formats(videoid: str):
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        try:
            info = ydl.extract_info(
                f"https://youtube.com/watch?v={videoid}", download=False
            )
        except Exception as e:
            print(f"Error extracting info: {e}")
            return None, None
        
        quality = 720
        format_id = None
        
        for f in info["formats"]:
            if f.get("height") == quality and f.get("ext") == "mp4":
                format_id = f["format_id"]
                break
        
        if not format_id:
            for f in info["formats"]:
                if f.get("height") and f.get("height") <= quality and f.get("ext") == "mp4":
                    format_id = f["format_id"]
                    quality = f["height"]
        
        if not format_id:
            format_id = "best[height<=720]"
        
        return format_id, quality


async def stream_from_link(link: str):
    ytdl_opts = {
        "format": "best[height<=720]/best",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }
    
    ydl = yt_dlp.YoutubeDL(ytdl_opts)
    try:
        info = ydl.extract_info(link, download=False)
        return info["url"]
    except Exception as e:
        print(f"Error in stream_from_link: {e}")
        return None