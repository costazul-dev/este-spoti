import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Dict, Any
import time
from config.settings import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_SCOPES
)

class SpotifyClient:
    def __init__(self):
        self.auth_manager = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=' '.join(SPOTIFY_SCOPES),
            open_browser=False
        )
        
        auth_url = self.auth_manager.get_authorize_url()
        
        print("\nSpotify Authentication Required:")
        print("1. Please visit this URL to authorize the application:")
        print(f"\n{auth_url}\n")
        print("2. After accepting, you'll be redirected to a localhost URL.")
        print("3. Copy the entire URL from your browser's address bar and paste it here.")
        
        response_url = input("\nPaste the URL here: ").strip()
        code = self.auth_manager.parse_response_code(response_url)
        self.auth_manager.get_access_token(code)
        
        self.client = spotipy.Spotify(auth_manager=self.auth_manager)
        self.user_id = self.client.current_user()['id']

    def test_connection(self):
        """Test the Spotify connection and credentials"""
        try:
            user = self.client.current_user()
            return f"Connected as: {user['display_name']} ({user['id']})"
        except Exception as e:
            return f"Connection failed: {str(e)}"

    def get_all_playlists(self) -> List[Dict[str, Any]]:
        playlists = []
        results = self.client.current_user_playlists(limit=50)
        playlists.extend(results['items'])
        
        while results['next']:
            results = self.client.next(results)
            playlists.extend(results['items'])
            time.sleep(0.1)  # Rate limiting prevention
        
        return playlists

    def get_playlist_tracks(self, playlist_id: str) -> List[Dict[str, Any]]:
        tracks = []
        results = self.client.playlist_tracks(playlist_id)
        tracks.extend(results['items'])
        
        while results['next']:
            try:
                results = self.client.next(results)
                tracks.extend(results['items'])
                time.sleep(0.1)  # Rate limiting prevention
            except Exception as e:
                print(f"Error fetching tracks: {str(e)}")
                time.sleep(1)  # Longer delay on error
                continue
        
        return tracks