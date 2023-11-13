"""
1. Bar plot/ pie chart about genres in playlist. (track.artist[genres])
                       ^^^^^^^^^^^^ note: w połowie, kurwa, nie ma takch danych
2. Average song duration in playlist. (audio_features[duration])
3. Bar plot about overall positiveness of playlist. (audio_features[valence])
4. Bar plot about overall energy of playlist. (audio_features[energy])
4. Bar plot about release years of songs.
5. Bar plot top 3 artists in playlist.

"""
import pandas as pd
from urllib.parse import urlparse, parse_qs

import models


async def validate_response(resp):
    if resp.status == 200:
        content_type = resp.headers.get('content-type')
        if 'application/json' not in content_type:
            raise TypeError(f"Response content-type !json. {content_type}")
        data = await resp.json()
        return data
    else:
        raise ValueError(f"Response status code is not 200: {resp.status}.\n {resp.headers}")


def get_total_playlist_duration(playlist: dict) -> float:
    total_duration = 0
    for i, track in enumerate(playlist['tracks']['items']):
        try:
            total_duration += track['track']['duration_ms']
        except TypeError:
            continue

    return total_duration


def ms_to_min_converter(duration_ms: int) -> float:
    secs = duration_ms / 1000
    min, sec_remainder = divmod(secs, 60)
    min = int(min)
    act_secs = int(round(sec_remainder))

    return min, act_secs


def ms_to_hh_mm(duration_ms):
    seconds, milliseconds = divmod(duration_ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    print(hours, ' : ', minutes)


def objects_to_dataframes(objects) -> pd.DataFrame:
    if isinstance(objects, list):
        return pd.DataFrame.from_records([o.__dict__ for o in objects])
    else:
        raise TypeError("The 'objects' argument should be a list of class instances.")

def dataframe_to_objects(dataframe: pd.DataFrame) -> list[models.Track]:
    all_tracks = []
    for i in range(1,len(dataframe)):
        all_tracks.append(models.Track(*dataframe.iloc[i]))

    return all_tracks


def save_to_file(dataframe: pd.DataFrame, name: str):
    dataframe.to_csv("playlists/" +name+"_playlist.csv", sep=';')


async def extract_playlist_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if 'si' in query_params:
        playlist_id = parsed_url.path.split('/')[-1]
        return playlist_id
    return None