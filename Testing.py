from random import shuffle
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up your Spotify API credentials
SPOTIPY_CLIENT_ID = '0d16d96047644a34bf896349652bcc93'
SPOTIPY_CLIENT_SECRET = 'cd17688e6f094311be5c00a85de8987b'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'playlist-modify-public user-top-read'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

def main():
    # Get user's top 50 tracks
    top_tracks = sp.current_user_top_tracks(limit=50)

    # Extract track IDs from top tracks
    top_track_ids = [track['id'] for track in top_tracks['items']]

    # Get recommended tracks
    recommended_tracks = []

    for track_id in top_track_ids:
        related_tracks = sp.recommendations(seed_tracks=[track_id], limit=5)
        recommended_tracks.extend([track['id'] for track in related_tracks['tracks']])

    # Create a new playlist for recommended tracks
    user_id = sp.current_user()['id']
    recommended_playlist = sp.user_playlist_create(user_id, name='Recommended Tracks', public=True)

    # Add recommended tracks to the playlist
    batch_size = 100
    for i in range(0, len(recommended_tracks), batch_size):
        batch_tracks = recommended_tracks[i:i + batch_size]
        sp.playlist_add_items(recommended_playlist['id'], batch_tracks)

    print('Playlists have been created!')