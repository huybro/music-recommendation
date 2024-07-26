from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from models import Base,Playlist,Track

def get_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

def initialize_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

def save_playlist_to_db(session, playlist_id, playlist_name, tracks):
    playlist = Playlist(playlist_id=playlist_id, name=playlist_name)
    session.add(playlist)
    session.commit()

    track_objects = []
    for track in tracks:
        track_obj = Track(
            track_id=track['Track ID'],
            name=track['Track Name'],
            artists=track['Artists'],
            album_name=track['Album Name'],
            album_id=track['Album ID'],
            popularity=track['Popularity'],
            release_date=track['Release Date'],
            duration_ms=track['Duration (ms)'],
            explicit=track['Explicit'],
            external_url=track['External URLs'],
            danceability=track['Danceability'],
            energy=track['Energy'],
            key=track['Key'],
            loudness=track['Loudness'],
            mode=track['Mode'],
            speechiness=track['Speechiness'],
            acousticness=track['Acousticness'],
            instrumentalness=track['Instrumentalness'],
            liveness=track['Liveness'],
            valence=track['Valence'],
            tempo=track['Tempo'],
            playlist_id=playlist.id
        )
        track_objects.append(track_obj)

    session.bulk_save_objects(track_objects)
    session.commit()