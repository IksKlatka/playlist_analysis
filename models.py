import datetime
from dataclasses import dataclass
from typing import List

@dataclass
class User:
    """
    Only for informational purposes, on the top of output.
    Username, user id.
    """
    id: int
    username: str
    pass


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
    """
    Track data like: artist, title, duration, genre
    """
    id: int
    name: str
    artist: str
    album: str
    album_release_date: str
    duration: int # in ms
    valence: float # from 0 to 1
    energy: float
    genres: list[str]



