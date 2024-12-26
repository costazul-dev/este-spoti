import os
from dotenv import load_dotenv

load_dotenv()

# Spotify API Settings
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
SPOTIFY_SCOPES = [
    'playlist-read-private',
    'playlist-read-collaborative',
    'user-library-read'
]

# Database Settings
DB_NAME = 'spotify_library.db'