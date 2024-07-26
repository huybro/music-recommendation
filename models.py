from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True)
    playlist_id = Column(String, unique=True, nullable=False)
    name = Column(String)
    tracks = relationship('Track', backref='playlist')

class Track(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    track_id = Column(String, unique=True, nullable=False)
    name = Column(String)
    artists = Column(String)
    album_name = Column(String)
    album_id = Column(String)
    popularity = Column(Integer)
    release_date = Column(Date)
    duration_ms = Column(Integer)
    explicit = Column(Boolean)
    external_url = Column(String)
    danceability = Column(Float)
    energy = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    speechiness = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    playlist_id = Column(Integer, ForeignKey('playlists.id'))
