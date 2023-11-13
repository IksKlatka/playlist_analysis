import datetime
from dataclasses import dataclass
from typing import Optional

# note: niepotrzebne
@dataclass
class User:
    """
    Only for informational purposes, on the top of output.
    Username, user id.
    """
    id: int
    username: str
    pass

# note: niepotrzebne
@dataclass
class Playlist:
    """
    Data about playlist, information like:
    name, duration, total songs, date created

    """
    id: int
    name: str
    author: str
    total_songs : int
    duration: int # in ms SUM(each(TRACK) duration)


@dataclass
class Track:
    id: int
    name: str
    artist: str
    album: str
    album_release_date: str
    duration: int # in ms
    valence: float # from 0 to 1
    energy: float # from 0 to 1
    tempo: float
    loudness: float # from -60dB to 0dB
    danceability: float # from 0 to 1
    genres: list[str]
    playlist_id: Optional[str] = None




