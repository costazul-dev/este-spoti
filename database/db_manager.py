import sqlite3
from datetime import datetime
from typing import List, Tuple
from .models import Playlist, Song, PlaylistSong

class DatabaseManager:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS playlists (
                playlist_id TEXT PRIMARY KEY,
                name TEXT,
                last_updated TIMESTAMP,
                total_tracks INTEGER,
                is_private BOOLEAN,
                owner_id TEXT,
                owner_name TEXT
            );
            
            CREATE TABLE IF NOT EXISTS songs (
                song_id TEXT PRIMARY KEY,
                name TEXT,
                artist TEXT,
                album TEXT,
                duration_ms INTEGER
            );
            
            CREATE TABLE IF NOT EXISTS playlist_songs (
                playlist_id TEXT,
                song_id TEXT,
                added_at TIMESTAMP,
                FOREIGN KEY (playlist_id) REFERENCES playlists (playlist_id),
                FOREIGN KEY (song_id) REFERENCES songs (song_id),
                PRIMARY KEY (playlist_id, song_id)
            );
        ''')
        self.conn.commit()
    
    def add_playlist(self, playlist: Playlist):
        self.cursor.execute('''
            INSERT OR REPLACE INTO playlists 
            (playlist_id, name, last_updated, total_tracks, is_private, owner_id, owner_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            playlist.playlist_id,
            playlist.name,
            playlist.last_updated,
            playlist.total_tracks,
            playlist.is_private,
            playlist.owner_id,
            playlist.owner_name
        ))
        self.conn.commit()

    def add_song(self, song: Song):
        self.cursor.execute('''
            INSERT OR REPLACE INTO songs 
            (song_id, name, artist, album, duration_ms)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            song.song_id,
            song.name,
            song.artist,
            song.album,
            song.duration_ms
        ))
        self.conn.commit()

    def add_playlist_song(self, playlist_song: PlaylistSong):
        self.cursor.execute('''
            INSERT OR REPLACE INTO playlist_songs 
            (playlist_id, song_id, added_at)
            VALUES (?, ?, ?)
        ''', (
            playlist_song.playlist_id,
            playlist_song.song_id,
            playlist_song.added_at
        ))
        self.conn.commit()

    def get_stats(self) -> Tuple[int, int, int]:
        self.cursor.execute('''
            WITH playlist_counts AS (
                SELECT 
                    COUNT(DISTINCT p.playlist_id) as total_playlists,
                    SUM(CASE WHEN p.is_private THEN 1 ELSE 0 END) as private_playlists
                FROM playlists p
            ),
            song_counts AS (
                SELECT COUNT(DISTINCT s.song_id) as unique_songs
                FROM songs s
            )
            SELECT 
                total_playlists,
                private_playlists,
                unique_songs
            FROM playlist_counts, song_counts
        ''')
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()