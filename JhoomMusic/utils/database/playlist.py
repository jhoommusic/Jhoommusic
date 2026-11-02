# Playlist helpers (in-memory stub)

playlists = {}

def save_playlist(user_id: int, name: str, tracks: list):
    if user_id not in playlists:
        playlists[user_id] = {}
    playlists[user_id][name] = tracks

def get_playlist(user_id: int, name: str):
    return playlists.get(user_id, {}).get(name, [])

def delete_playlist(user_id: int, name: str):
    if user_id in playlists and name in playlists[user_id]:
        del playlists[user_id][name]

def get_user_playlists(user_id: int):
    return list(playlists.get(user_id, {}).keys())
