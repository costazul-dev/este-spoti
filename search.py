import sqlite3
from datetime import datetime
import sys

def search_songs(query):
    conn = sqlite3.connect('spotify_library.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT DISTINCT 
                s.name as song_name,
                s.artist,
                p.name as playlist_name,
                p.is_private,
                ps.added_at,
                p.owner_id,
                p.owner_name
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            JOIN playlists p ON ps.playlist_id = p.playlist_id
            WHERE s.name LIKE ? 
               OR s.artist LIKE ?
            ORDER BY ps.added_at DESC
        ''', (f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        
        if not results:
            print(f"\nNo songs found matching '{query}'")
            return
        
        songs = {}
        for row in results:
            song_name, artist, playlist_name, is_private, added_at, owner_id, owner_name = row
            key = (song_name, artist)
            if key not in songs:
                songs[key] = {'owned': [], 'followed': []}
            
            playlist_info = (playlist_name, is_private, added_at, owner_name)
            if owner_id == 'your_spotify_id':  # Will be automatically set to your ID when running main.py
                songs[key]['owned'].append(playlist_info)
            else:
                songs[key]['followed'].append(playlist_info)
        
        print(f"\nFound {len(songs)} matching songs:\n")
        
        for (song_name, artist), playlists in songs.items():
            print(f"Song: {song_name}")
            print(f"Artist: {artist}")
            
            if playlists['owned']:
                print("\nIn your playlists:")
                for name, is_private, added_at, _ in playlists['owned']:
                    privacy = "Private" if is_private else "Public"
                    added_date = datetime.fromisoformat(added_at.replace('Z', '+00:00'))
                    print(f"  - {name} ({privacy}) - Added: {added_date.strftime('%Y-%m-%d')}")
            
            if playlists['followed']:
                print("\nIn followed playlists:")
                for name, is_private, added_at, owner in playlists['followed']:
                    privacy = "Private" if is_private else "Public"
                    added_date = datetime.fromisoformat(added_at.replace('Z', '+00:00'))
                    print(f"  - {name} by {owner} ({privacy}) - Added: {added_date.strftime('%Y-%m-%d')}")
            print()

    finally:
        conn.close()

if __name__ == "__main__":
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter song or artist to search for: ")
    search_songs(query)