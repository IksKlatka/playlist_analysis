import asyncio
import datetime

import pandas as pd
from collections import Counter

import additional_functions
from gather_data import get_user_info, get_playlist_items
import matplotlib.pyplot as plt

def objects_to_dataframes(objects) -> pd.DataFrame:
    if isinstance(objects, list):
        return pd.DataFrame.from_records([o.__dict__ for o in objects])
    else:
        raise TypeError("The 'objects' argument should be a list of class instances.")


def get_avg_playlist_energy(dataframe: pd.DataFrame):
    """Range from 0 to 1. Closer to 1 == higher in energy"""
    mean_energy = round(dataframe['energy'].mean(), 3)
    print(f"Mean energy of this playlist is {mean_energy}.")

    if mean_energy <= 0.25:
        print("Zzz....")
    elif mean_energy > 0.25 and mean_energy <= 0.5:
        print("Low energy.")
    elif mean_energy > 0.5 and mean_energy <= 0.75:
        print("Moderate energy.")
    else:
        print("Big energy.")

    sorted_df = dataframe.sort_values(by='energy', ascending=False)
    top_10 = sorted_df.head(10)

    print(f"The most energetic song in playlist is: {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} "
          f"with energy = {sorted_df.iloc[0]['energy']}")
    print(f"The least energetic song in playlist is: {sorted_df.iloc[-1]['name']} by {sorted_df.iloc[-1]['artist']} "
          f"with energy = {sorted_df.iloc[-1]['energy']}")

    plt.figure(figsize=(7, 6))
    plt.bar(top_10['artist'], top_10['energy'])
    plt.ylabel("Energy")
    plt.xlabel("Artist")
    plt.title("Energy levels of songs in the playlist.")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()


def get_avg_playlist_valence(dataframe: pd.DataFrame): # positivity
    """Range from 0 to 1. Closer to 1 == higher positiveness"""
    mean_valence = round(dataframe['valence'].mean(), 3)
    print(f"Mean positiveness of this playlist is equal to: {mean_valence}")
    if mean_valence <= 0.25:
        print("Depressive")
    elif mean_valence > 0.25 and mean_valence <= 0.5:
        print("Nostalgic")
    elif mean_valence > 0.5 and mean_valence <= 0.75:
        print("Moderate")
    else:
        print("Positive")

    sorted_df = dataframe.sort_values(by='valence', ascending=False)
    top_10 = sorted_df.head(10)

    plt.figure(figsize=(7, 6))
    plt.bar(top_10['artist'], top_10['valence'])
    plt.ylabel("Valence")
    plt.xlabel("Artist")
    plt.title("Valence levels of songs in the playlist.")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()

#todo: think about how to plot this
def get_avg_track_duration(dataframe: pd.DataFrame) -> int:
    mean_track_duration = dataframe['duration'].mean()
    additional_functions.ms_to_min_converter(mean_track_duration)

    short_tracks = len(dataframe.loc[dataframe['duration'] < mean_track_duration])
    print(f"Which is longer than {(short_tracks*100/len(dataframe)):.0f}% of playlist songs.")


def get_common_release_years_of_tracks(dataframe: pd.DataFrame):
    dataframe['album_release_date'] = pd.to_datetime(dataframe['album_release_date']).dt.date
    sorted_df = dataframe.sort_values(by="album_release_date", ascending=False)

    over_2020 = sorted_df.loc[sorted_df['album_release_date'] >= datetime.date(2001, 1, 1)]
    before_2020 = sorted_df.loc[sorted_df['album_release_date'] < datetime.date(2001, 1, 1)]

    release_years = Counter([date.year for date in sorted_df['album_release_date']])
    print(release_years)

    plt.bar(release_years.keys(), release_years.values())
    plt.xlabel("Years")
    plt.ylabel("Count")
    plt.title("Tracks release years.")
    plt.tight_layout()
    plt.show()


def get_top_playlist_artists(dataframe: pd.DataFrame):

    artist_count = Counter(dataframe['artist'])
    most_common = artist_count.most_common(3)

    artist, count = zip(*most_common)

    plt.bar(artist, count)
    plt.ylabel("Songs count")
    plt.xlabel("Artists")
    plt.title("Most common artists in playlist.")
    plt.show()



async def _main():
    # user_id = 'iga.klatka'
    # playlist_id = '3hq8qM0t1YdggfEbEdntjn'
    #
    # # tracks, playlist = await get_playlist_items(playlist_id=playlist_id)
    # # track_df = objects_to_dataframes(tracks)
    # # track_df.to_csv("tracks.csv", sep=";")

    track_df = pd.DataFrame(pd.read_csv("sample_tracks.csv", sep=";", index_col=0))

    #todo:
    #   save fetched data into CSV file - to limit API requests [X]
    #   interactiveness [X]


    #done:
    #   get_avg_playlist_energy(dataframe=track_df)
    #   get_avg_playlist_valence(dataframe=track_df)
    #   get_avg_track_duration(dataframe=track_df)
    #   get_common_release_years_of_tracks(dataframe=track_df)
    #   get_top_playlist_artists(dataframe=track_df)



if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    asyncio.run(main=_main())
