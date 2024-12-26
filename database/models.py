from dataclasses import dataclass
from datetime import datetime

@dataclass
class Playlist:
    playlist_id: str
    name: str
    last_updated: datetime
    total_tracks: int
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