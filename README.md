# este-spoti: Personal Spotify Library Analytics

A Python-based tool for synchronizing and analyzing your Spotify listening data. The application captures your music library periodically and stores it in a local SQLite database, enabling personal analytics and custom reporting of your listening patterns over time.

## Key Features

- **Automated Library Synchronization**: Regular capture of your Spotify library data
- **Local Data Storage**: Secure SQLite database for offline analysis
- **Metadata Tracking**: Comprehensive tracking of playlists and track information
- **Search Capabilities**: Efficient search functionality across your entire music collection
- **Analytics Foundation**: Framework for generating custom listening reports and insights

## Technology Stack

This project is built with:
- Python
- Spotipy (Spotify Web API client)
- SQLite

## Getting Started

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Spotify API credentials in `.env`:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   ```
4. Run the synchronization:
   ```bash
   python main.py
   ```

## Project Structure

The project maintains a clear separation of concerns:
- `spotify/`: Spotify API interaction logic
- `database/`: Database management and models
- `utils/`: Helper functions and utilities
- `config/`: Configuration management

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with Spotify Web API and inspired by the need for personal music listening analytics.

---
*Note: This project is designed for personal data analytics and music library management.*
