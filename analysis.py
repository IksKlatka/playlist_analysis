import asyncio
import datetime
import pandas as pd
from collections import Counter
import additional_functions
import matplotlib.pyplot as plt

from additional_functions import ms_to_min_converter

def objects_to_dataframes(objects) -> pd.DataFrame:
    if isinstance(objects, list):
        return pd.DataFrame.from_records([o.__dict__ for o in objects])
    else:
        raise TypeError("The 'objects' argument should be a list of class instances.")


def get_avg_playlist_energy(dataframe: pd.DataFrame):
    """Range from 0 to 1. Closer to 1 == higher in energy"""
    print("Tracks energy insights.\n")
    mean_energy = round(dataframe['energy'].mean(), 3)
    def energy_level(mean_energy):
        if mean_energy <= 0.25:
            return "Zzz...."
        elif mean_energy > 0.25 and mean_energy <= 0.5:
            return "Low energy."
        elif mean_energy > 0.5 and mean_energy <= 0.75:
            return "Moderate energy.\n"
        else:
            return "Big energy.\n"

    sorted_df = dataframe.sort_values(by='energy', ascending=False)
    more_energy = len(dataframe.loc[dataframe['energy'] >= mean_energy])
    top_24 = sorted_df.head(24)

    print(f"""
    Mean energy of this playlist is {mean_energy}, which is {energy_level(mean_energy)}.
    About {((more_energy*100)/len(dataframe)):.1f}% of tracks have higher or equal energy level to mean value.
    The most energetic song in playlist is: {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} with energy = {sorted_df.iloc[0]['energy']}
    The least energetic song in playlist is: {sorted_df.iloc[-1]['name']} by {sorted_df.iloc[-1]['artist']} with energy = {sorted_df.iloc[-1]['energy']}
    """)

    colors = ['g' if v >= 0.75 else ('y' if v >= 0.5 and v < 0.75 else 'r') for v in top_24['energy']]
    plt.figure(figsize=(7, 6))
    plt.bar(top_24['artist'], top_24['energy'], color=colors)
    plt.ylabel("Energy")
    plt.xlabel("Artist")
    plt.title("Energy levels of Top25 tracks in the playlist.")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()

def get_avg_playlist_valence(dataframe: pd.DataFrame): # positivity
    """Range from 0 to 1. Closer to 1 == higher positiveness"""
    print("Tracks mood insights.\n")
    mean_valence = round(dataframe['valence'].mean(), 3)
    more_positive = len(dataframe.loc[dataframe['valence'] > mean_valence])
    sorted_df = dataframe.sort_values(by='valence', ascending=False)
    def mood(mean_valence: float):
        if mean_valence <= 0.25:
            return "quite depressive."
        elif mean_valence > 0.25 and mean_valence <= 0.5:
            return "a bit nostalgic."
        elif mean_valence > 0.5 and mean_valence <= 0.75:
            return "moderate."
        else:
            return "positive."

    print(f"""
    Mean positiveness of this playlist is equal to: {mean_valence}, which is {mood(mean_valence)}
    About {((more_positive*100)/len(dataframe)):.1f}% of tracks have higher valence than the mean value.
    Most positive track on the playlist is {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} with valence = {sorted_df.iloc[0]['valence']}.
    Most depressive track on the playlist is {sorted_df.iloc[-1]['name']} by {sorted_df.iloc[-1]['artist']} with valence = {sorted_df.iloc[-1]['valence']}.\n
    """)

    top_24 = sorted_df.head(24)
    colors = ['#0cb800' if v >= 0.75 else ('#fb0' if v >= 0.5 and v < 0.75 else '#ff009d') for v in top_24['valence']]
    plt.figure(figsize=(7, 6))
    plt.bar(top_24['artist'], top_24['valence'], color=colors)
    plt.ylabel("Valence")
    plt.xlabel("Artist")
    plt.title("Valence levels of Top25 tracks in the playlist.")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()

def get_avg_track_duration(dataframe: pd.DataFrame) -> int:
    print("Tracks duration insights.")
    total_duration = dataframe['duration'].sum()
    mean_track_duration = dataframe['duration'].mean()
    short_tracks = len(dataframe.loc[dataframe['duration'] < mean_track_duration])
    sorted_df = dataframe.sort_values(by='duration', ascending=False)
    longest_track = sorted_df.iloc[0]['name']
    shortest_track = sorted_df.iloc[-1]['name']

    longest_min, longest_sec = ms_to_min_converter(sorted_df.iloc[0]['duration'])
    shortest_min, shortest_sec = ms_to_min_converter(sorted_df.iloc[-1]['duration'])
    mean_min, mean_secs = ms_to_min_converter(mean_track_duration)
    tot_min, tot_secs = ms_to_min_converter(total_duration)

    print(f"""
    Total playlist duration = {tot_min}min {tot_secs}s.
    Mean track duration = {mean_min}min {mean_secs}s.
    Which is longer than {(short_tracks*100/len(dataframe)):.0f}% of playlist songs.\n
    Longest song is '{longest_track}' by {sorted_df.iloc[0]['artist']} with duration = {longest_min}min {longest_sec}s,
    and it takes {((sorted_df.iloc[0]['duration'] * 100)/ total_duration):.1f}% of whole playlist duration.
    The shortest, on the other hand, is '{shortest_track}' by {sorted_df.iloc[-1]['artist']} with 
    duration = {shortest_min}min {shortest_sec}s, takes {((sorted_df.iloc[-1]['duration'] * 100)/ total_duration):.1f}% of whole playlist duration.\n\n
    """)

    if len(sorted_df) > 25:
        durations = sorted_df['duration'][:25]
        labels = sorted_df['name'][:25]
    else:
        durations = sorted_df['duration']
        labels = sorted_df['name']

    explodes = [0.1 for _ in range(len(durations))]
    explodes[0] = 0.2
    plt.figure(figsize=(8, 8))
    patches, labels, pct_texts = plt.pie(durations, labels=labels, autopct='%1.1f%%', rotatelabels=True, explode=explodes)
    plt.title('Percent of tracks duration of playlist.')

    for label, pct_text in zip(labels, pct_texts):
        pct_text.set_rotation(label.get_rotation())
    plt.show()

def get_common_release_years_of_tracks(dataframe: pd.DataFrame):
    print("Tracks albums release years insights.\n")

    dataframe['album_release_date'] = pd.to_datetime(dataframe['album_release_date']).dt.date
    sorted_df = dataframe.sort_values(by="album_release_date", ascending=False)
    release_years = Counter([date.year for date in sorted_df['album_release_date']])
    over_2020 = sorted_df.loc[sorted_df['album_release_date'] >= datetime.date(2020, 1, 1)]
    colors = ['g' if v >= 20 else ('y' if v >= 10 and v < 5 else 'c') for v in release_years.values()]

    print(f"""
    About {((len(over_2020)*100)/ len(dataframe)):.1f}% of albums were released after year 2020.\n
    Newest track on the playlist is {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} 
    released on {sorted_df.iloc[0]['album_release_date']}. The oldest track, on the other hand, is {sorted_df.iloc[-1]['name']} 
    by {sorted_df.iloc[-1]['artist']} released on {sorted_df.iloc[-1]['album_release_date']}.\n\n
    """)

    plt.bar(release_years.keys(), release_years.values(), color=colors)
    plt.xlabel("Years")
    plt.ylabel("Released tracks count.")
    plt.title("Tracks count by release years.")
    plt.xticks(list(map(int, release_years.keys())), rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def get_top_playlist_artists(dataframe: pd.DataFrame):
    print("Artist insights.")
    artist_count = Counter(dataframe['artist'])
    most_common = artist_count.most_common(10)
    artist, count = zip(*most_common)
    overall_min, overall_secs = ms_to_min_converter(dataframe['duration'].sum())

    one_trackers = [a for a, c in artist_count.items() if c == 1]
    one_trackers_data = dataframe[dataframe['artist'].isin(one_trackers)]
    top_1 = dataframe[dataframe['artist'] == artist[0]]['duration'].sum()
    top_min, top_secs = ms_to_min_converter(top_1)
    one_min, one_secs = ms_to_min_converter(one_trackers_data['duration'].sum())

    print(f"""
    Most common artist, {artist[0]}, takes about {((artist_count[artist[0]]*100)/len(dataframe)):.1f}% of all 
    artists in the playlist and their sum of track duration = {top_min}min {top_secs}s.\n
    About {((len(one_trackers)*100)/len(dataframe)):.1f}% of artists own one song on the playlist,
    and they owe {one_min}min {one_secs}s in playlist.
    Out of total {overall_min}min {overall_secs}s playlist duration.
    """)

    colors = ['#0cb800' if c > 10 else ('#fb0' if c > 5 else '#ff009d') for c in count]
    plt.bar(artist, count, color=colors)

    plt.ylabel("Songs count")
    plt.xlabel("Artists")
    plt.title("10 most common artists in playlist.")

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

async def _main():
    user_id = 'iga.klatka'
    playlist_id = '3hq8qM0t1YdggfEbEdntjn'


    track_df = pd.DataFrame(pd.read_csv("books.mp3.csv", sep=";", index_col=0))

    #todo:
    #   interactiveness [0]


    #done:

    # get_common_release_years_of_tracks(dataframe=track_df)
    # get_top_playlist_artists(dataframe=track_df)


    get_avg_playlist_valence(dataframe=track_df)
    # get_avg_playlist_energy(dataframe=track_df)
    # get_avg_track_duration(dataframe=track_df)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    asyncio.run(main=_main())
