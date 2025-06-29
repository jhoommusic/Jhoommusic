from typing import Dict, List
from JhoomMusic.utils.database.database import temp_db

playlistdb = temp_db.playlist


async def get_playlist_names(user_id: int) -> List[str]:
    """Get all playlist names for user"""
    results = []
    async for playlist in playlistdb.find({"user_id": user_id}):
        results.append(playlist["playlist_name"])
    return results


async def get_playlist(user_id: int, playlist_name: str) -> List[Dict]:
    """Get playlist tracks"""
    playlist = await playlistdb.find_one({
        "user_id": user_id, 
        "playlist_name": playlist_name
    })
    if not playlist:
        return []
    return playlist.get("tracks", [])


async def save_playlist(user_id: int, playlist_name: str, tracks: List[Dict]):
    """Save playlist"""
    await playlistdb.update_one(
        {"user_id": user_id, "playlist_name": playlist_name},
        {"$set": {"tracks": tracks}},
        upsert=True
    )


async def delete_playlist(user_id: int, playlist_name: str):
    """Delete playlist"""
    await playlistdb.delete_one({
        "user_id": user_id, 
        "playlist_name": playlist_name
    })


async def add_to_playlist(user_id: int, playlist_name: str, track: Dict):
    """Add track to playlist"""
    playlist = await playlistdb.find_one({
        "user_id": user_id, 
        "playlist_name": playlist_name
    })
    
    if not playlist:
        await playlistdb.insert_one({
            "user_id": user_id,
            "playlist_name": playlist_name,
            "tracks": [track]
        })
    else:
        tracks = playlist.get("tracks", [])
        tracks.append(track)
        await playlistdb.update_one(
            {"user_id": user_id, "playlist_name": playlist_name},
            {"$set": {"tracks": tracks}}
        )


async def remove_from_playlist(user_id: int, playlist_name: str, track_index: int):
    """Remove track from playlist"""
    playlist = await playlistdb.find_one({
        "user_id": user_id, 
        "playlist_name": playlist_name
    })
    
    if playlist and "tracks" in playlist:
        tracks = playlist["tracks"]
        if 0 <= track_index < len(tracks):
            tracks.pop(track_index)
            await playlistdb.update_one(
                {"user_id": user_id, "playlist_name": playlist_name},
                {"$set": {"tracks": tracks}}
            )