import aiohttp
import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from JhoomMusic import app
from JhoomMusic.utils.pastebin import paste
from config import BANNED_USERS

# Lyrics APIs
LYRICS_APIS = [
    "https://api.lyrics.ovh/v1/{artist}/{title}",
    "https://some-random-api.ml/lyrics?title={title}",
]

@app.on_message(filters.command(["lyrics", "lyric"]) & filters.group)
async def get_lyrics(client, message: Message):
    """Get song lyrics"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/lyrics <song name>` - Get lyrics\n"
            "• `/lyrics <artist> - <song>` - Get specific lyrics\n\n"
            "**Examples:**\n"
            "• `/lyrics Imagine Dragons Believer`\n"
            "• `/lyrics Ed Sheeran - Shape of You`"
        )
    
    query = " ".join(message.command[1:])
    mystic = await message.reply_text(f"🔍 **Searching lyrics for:** {query}")
    
    try:
        # Parse artist and title
        if " - " in query:
            artist, title = query.split(" - ", 1)
            artist = artist.strip()
            title = title.strip()
        else:
            # Try to guess artist and title
            parts = query.split()
            if len(parts) >= 2:
                artist = parts[0]
                title = " ".join(parts[1:])
            else:
                artist = ""
                title = query
        
        lyrics = await search_lyrics(artist, title)
        
        if lyrics:
            # Check if lyrics are too long
            if len(lyrics) > 4000:
                # Upload to pastebin
                paste_url = await paste(lyrics, f"Lyrics: {artist} - {title}")
                if paste_url:
                    await mystic.edit_text(
                        f"📝 **Lyrics Found!**\n\n"
                        f"**Song:** {title}\n"
                        f"**Artist:** {artist}\n\n"
                        f"**Lyrics are too long, uploaded to:** {paste_url}",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("📝 View Lyrics", url=paste_url)]
                        ])
                    )
                else:
                    await mystic.edit_text(
                        f"📝 **Lyrics Found!**\n\n"
                        f"**Song:** {title}\n"
                        f"**Artist:** {artist}\n\n"
                        f"**Note:** Lyrics are too long to display here."
                    )
            else:
                await mystic.edit_text(
                    f"📝 **Lyrics Found!**\n\n"
                    f"**Song:** {title}\n"
                    f"**Artist:** {artist}\n\n"
                    f"```\n{lyrics}\n```"
                )
        else:
            await mystic.edit_text(
                f"❌ **No lyrics found for:** {query}\n\n"
                f"**Try:**\n"
                f"• Different spelling\n"
                f"• Artist name - Song name format\n"
                f"• More specific search terms"
            )
    
    except Exception as e:
        await mystic.edit_text(f"❌ **Error searching lyrics:** {str(e)}")

async def search_lyrics(artist: str, title: str) -> str:
    """Search for lyrics using multiple APIs"""
    
    # Clean up artist and title
    artist = artist.replace(" ", "%20")
    title = title.replace(" ", "%20")
    
    async with aiohttp.ClientSession() as session:
        # Try lyrics.ovh API
        try:
            url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if "lyrics" in data and data["lyrics"]:
                        return data["lyrics"].strip()
        except:
            pass
        
        # Try some-random-api
        try:
            url = f"https://some-random-api.ml/lyrics?title={title}"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if "lyrics" in data and data["lyrics"]:
                        return data["lyrics"].strip()
        except:
            pass
        
        # Try genius API (if available)
        try:
            search_query = f"{artist} {title}".replace("%20", " ")
            url = f"https://api.genius.com/search?q={search_query}"
            headers = {"Authorization": "Bearer YOUR_GENIUS_TOKEN"}  # Add your token
            
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("response", {}).get("hits"):
                        # This would require additional scraping
                        # For now, just return None
                        pass
        except:
            pass
    
    return None

@app.on_message(filters.command(["lyrics", "lyric"]) & filters.group)
async def get_song_info(client, message: Message):
    """Get detailed song information"""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/songinfo <song name>`\n\n"
            "**Example:** `/songinfo Imagine Dragons Believer`"
        )
    
    query = " ".join(message.command[1:])
    mystic = await message.reply_text(f"🔍 **Getting song info for:** {query}")
    
    try:
        # Search for song info using Last.fm API or similar
        song_info = await search_song_info(query)
        
        if song_info:
            info_text = f"🎵 **Song Information**\n\n"
            info_text += f"**Title:** {song_info.get('title', 'Unknown')}\n"
            info_text += f"**Artist:** {song_info.get('artist', 'Unknown')}\n"
            info_text += f"**Album:** {song_info.get('album', 'Unknown')}\n"
            info_text += f"**Duration:** {song_info.get('duration', 'Unknown')}\n"
            info_text += f"**Release Date:** {song_info.get('release_date', 'Unknown')}\n"
            info_text += f"**Genre:** {song_info.get('genre', 'Unknown')}\n"
            
            if song_info.get('description'):
                info_text += f"\n**Description:**\n{song_info['description'][:200]}..."
            
            buttons = []
            if song_info.get('youtube_url'):
                buttons.append([InlineKeyboardButton("🎵 Play on YouTube", url=song_info['youtube_url'])])
            if song_info.get('spotify_url'):
                buttons.append([InlineKeyboardButton("🎧 Play on Spotify", url=song_info['spotify_url'])])
            
            await mystic.edit_text(
                info_text,
                reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
            )
        else:
            await mystic.edit_text(f"❌ **No information found for:** {query}")
    
    except Exception as e:
        await mystic.edit_text(f"❌ **Error getting song info:** {str(e)}")

async def search_song_info(query: str) -> dict:
    """Search for song information"""
    
    # This is a placeholder function
    # You can implement actual API calls to Last.fm, Spotify, etc.
    
    try:
        async with aiohttp.ClientSession() as session:
            # Example: Last.fm API call
            api_key = "YOUR_LASTFM_API_KEY"  # Add your API key
            url = f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={query}&api_key={api_key}&format=json"
            
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    tracks = data.get("results", {}).get("trackmatches", {}).get("track", [])
                    
                    if tracks:
                        track = tracks[0] if isinstance(tracks, list) else tracks
                        return {
                            "title": track.get("name"),
                            "artist": track.get("artist"),
                            "album": "Unknown",
                            "duration": "Unknown",
                            "release_date": "Unknown",
                            "genre": "Unknown"
                        }
    except:
        pass
    
    return None