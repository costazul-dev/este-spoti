from typing import Dict, Any
from datetime import datetime
from database.models import Playlist, Song, PlaylistSong

def create_playlist_from_spotify_data(playlist_data: Dict[str, Any], spotify_modified: str) -> Playlist:
    current_time = datetime.now()
    return Playlist(
        playlist_id=playlist_data['id'],
        name=playlist_data['name'],
        last_updated=current_time,
        last_synced=current_time,  # New field
        spotify_modified_at=spotify_modified,  # New field
        total_tracks=playlist_data['tracks']['total'],
        previous_tracks=playlist_data['tracks']['total'],  # New field
        is_private=not playlist_data.get('public', True),
        owner_id=playlist_data['owner']['id'],
        owner_name=playlist_data['owner']['display_name']
    )

def create_song_from_spotify_data(track_data: Dict[str, Any]) -> Song:
    return Song(
        song_id=track_data['id'],
        name=track_data['name'],
        artist=track_data['artists'][0]['name'],
        album=track_data['album']['name'],
        duration_ms=track_data['duration_ms']
    )

def create_playlist_song_from_spotify_data(playlist_id: str, track_data: Dict[str, Any]) -> PlaylistSong:
    return PlaylistSong(
        playlist_id=playlist_id,
        song_id=track_data['track']['id'],
        added_at=datetime.fromisoformat(track_data['added_at'].replace('Z', '+00:00'))
    )