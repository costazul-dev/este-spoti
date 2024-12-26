# main.py
from tqdm import tqdm
import time
import sys
from datetime import datetime
from pathlib import Path
import logging
from config.settings import DB_NAME
from database.db_manager import DatabaseManager
from spotify.spotify_client import SpotifyClient
from utils.helpers import (
    create_playlist_from_spotify_data,
    create_song_from_spotify_data,
    create_playlist_song_from_spotify_data
)

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        filename=log_dir / f"spotify_sync_{datetime.now().strftime('%Y%m')}.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def sync_library():
    setup_logging()
    logging.info("Starting Spotify library sync")
    
    try:
        spotify = SpotifyClient()
        db = DatabaseManager(DB_NAME)
        
        # Test connection and log user info
        connection_status = spotify.test_connection()
        logging.info(connection_status)

        # Fetch all playlists
        playlists = spotify.get_all_playlists()
        total_playlists = len(playlists)
        logging.info(f"Found {total_playlists} playlists")
        
        # Initialize progress bar
        progress = tqdm(
            total=total_playlists,
            desc="Syncing Library",
            bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} playlists'
        )
        
        total_tracks = 0
        for playlist in playlists:
            try:
                # Process playlist
                playlist_model = create_playlist_from_spotify_data(playlist)
                db.add_playlist(playlist_model)
                
                # Process tracks
                tracks = spotify.get_playlist_tracks(playlist['id'])
                for track in tracks:
                    if not track['track'] or not track['track']['id']:
                        continue
                        
                    song_model = create_song_from_spotify_data(track['track'])
                    db.add_song(song_model)
                    
                    playlist_song_model = create_playlist_song_from_spotify_data(
                        playlist['id'],
                        track
                    )
                    db.add_playlist_song(playlist_song_model)
                    total_tracks += 1
                
                progress.update(1)
                
            except Exception as e:
                logging.error(f"Error processing playlist '{playlist['name']}': {str(e)}")
                time.sleep(1)
                continue
        
        # Log final statistics
        stats = db.get_stats()
        logging.info(f"""
Sync completed successfully:
- Total playlists processed: {stats[0]}
- Private playlists: {stats[1]}
- Unique songs: {stats[2]}
- Total tracks processed: {total_tracks}
        """)
        
        progress.close()
        db.close()
        
    except Exception as e:
        logging.error(f"Sync failed: {str(e)}")
        raise

if __name__ == "__main__":
    sync_library()