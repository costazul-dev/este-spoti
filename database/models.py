from dataclasses import dataclass
from datetime import datetime

@dataclass
class Playlist:
    playlist_id: str
    name: str
    last_updated: datetime
    last_synced: datetime      # When we last synced this playlist
    spotify_modified_at: str   # When Spotify last modified it
    total_tracks: int
    previous_tracks: int       # Track count from last sync
    is_private: bool
    owner_id: str
    owner_name: str

@dataclass
class Song:
    song_id: str
    name: str
    artist: str
    album: str
    duration_ms: int

@dataclass
class PlaylistSong:
    playlist_id: str
    song_id: str
    added_at: datetime