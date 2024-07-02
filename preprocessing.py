import spotipy
from spotipy.oauth2 import SpotifyOAuth
from main import access_token 
import pandas as pd

def get_data(playlist_id, access_token):
    sp = spotipy.Spotify(auth=access_token)

    playlist_tracks = sp.playlist_tracks(playlist_id, fields='items(track(id, name, artists, album(id, name)))')
    data = []
    for track_info in playlist_tracks['items']:
        track = track_info['track']
        audio_features = sp.audio_features(track['id'])[0] if  track['id'] != 'Not available' else None

        try:
            album_info = sp.album(track['album']['id']) if track['album']['id'] != 'Not available' else None
            release_date = album_info['release_date'] if album_info else None
        except: 
            release_date = None

        # Get popularity of the track
        try:
            track_info = sp.track(track['id']) if track['id'] != 'Not available' else None
            popularity = track_info['popularity'] if track_info else None
        except:
            popularity = None
            
        track_data = {
            'Track Name': track['name'],
            'Artists':  ', '.join([artist['name'] for artist in track['artists']]),
            'Album Name': track['album']['name'],
            'Album ID': track['album']['id'],
            'Track ID': track['id'],
            'Popularity': popularity,
            'Release Date': release_date,
            'Duration (ms)': audio_features['duration_ms'] if audio_features else None,
            'Explicit': track_info.get('explicit', None),
            'External URLs': track_info.get('external_urls', {}).get('spotify', None),
            'Danceability': audio_features['danceability'] if audio_features else None,
            'Energy': audio_features['energy'] if audio_features else None,
            'Key': audio_features['key'] if audio_features else None,
            'Loudness': audio_features['loudness'] if audio_features else None,
            'Mode': audio_features['mode'] if audio_features else None,
            'Speechiness': audio_features['speechiness'] if audio_features else None,
            'Acousticness': audio_features['acousticness'] if audio_features else None,
            'Instrumentalness': audio_features['instrumentalness'] if audio_features else None,
            'Liveness': audio_features['liveness'] if audio_features else None,
            'Valence': audio_features['valence'] if audio_features else None,
            'Tempo': audio_features['tempo'] if audio_features else None,
        }
        data.append(track_data)
    df = pd.DataFrame(data)
    return df
    
playlist_id = '37i9dQZF1E39wSQy5h80F6'
music_df = get_data(playlist_id, access_token)

