import os

import asyncio
import datetime
from dotenv import load_dotenv

from plots import *
from additional_functions import ms_to_min_converter

def objects_to_dataframes(objects) -> pd.DataFrame:
    if isinstance(objects, list):
        return pd.DataFrame.from_records([o.__dict__ for o in objects])
    else:
        raise TypeError("The 'objects' argument should be a list of class instances.")


def get_common_stat_data(data: pd.DataFrame, column: str):
    print(f"Tracks {column} insights.")

    mean = round(data[column].mean(), 3)
    higher = len(data.loc[data[column] >= mean])
    sorted = data.sort_values(by=column, ascending=False)

    return mean, higher, sorted

# done: done: done
def get_track_features_data(dataframe: pd.DataFrame):
    """
    Insights of tracks features such as:
    - tempo, - energy, - valence, - danceability, - loudness
    returning information about means, correlation, extremes,
    """

    if len(dataframe) > 25:
        print("Because of size of the playlist, graph visualizations won't cover all of the tracks.\n")

    def levels(mean_val):
        if mean_val <= 0.25:
            return "very low"
        elif mean_val > 0.25 and mean_val <= 0.5:
            return "low"
        elif mean_val > 0.5 and mean_val <= 0.75:
            return "moderate"
        else:
            return "high"


    #note: energy
    print("Tracks energy insights.")
    mean_energy, higher_energy, sorted_energy = get_common_stat_data(data=dataframe, column='energy')
    print(f"""
    Mean energy of this playlist is {mean_energy}, which is {levels(mean_energy)} energy.
    About {((higher_energy*100)/len(dataframe)):.1f}% of tracks have higher or equal energy level to mean value.
    The most energetic song in playlist is: {sorted_energy.iloc[0]['name']} by {sorted_energy.iloc[0]['artist']} with energy = {sorted_energy.iloc[0]['energy']}
    The least energetic song in playlist is: {sorted_energy.iloc[-1]['name']} by {sorted_energy.iloc[-1]['artist']} with energy = {sorted_energy.iloc[-1]['energy']}
    """)
    first_24 = sorted_df.head(24)

    # note: valence
    print("Tracks mood insights.")
    mean_valence, higher_valence, sorted_valence = get_common_stat_data(data=dataframe, column='valence')
    print(f"""
    Mean positiveness of this playlist is equal to: {mean_valence}, which is {levels(mean_valence)} valence.
    About {((higher_valence*100)/len(dataframe)):.1f}% of tracks have higher valence than the mean value.
    Most positive track on the playlist is {sorted_valence.iloc[0]['name']} by {sorted_valence.iloc[0]['artist']} with valence = {sorted_valence.iloc[0]['valence']}.
    Most depressive track on the playlist is {sorted_valence.iloc[-1]['name']} by {sorted_valence.iloc[-1]['artist']} with valence = {sorted_valence.iloc[-1]['valence']}.\n
    """)

    # note: danceability
    print("Tracks danceability insights.")
    mean_danceability, higher_danceability, sorted_danceability = get_common_stat_data(data=dataframe, column='danceability')
    print(f"""
    Mean danceability of playlist is equal to: {mean_danceability}, which is {levels(mean_danceability)} danceability.
    Tracks with danceability higher or equal take up to {((higher_danceability*100)/len(dataframe)):.1f}% of playlist.
    Most danceable track is {sorted_danceability.iloc[0]['name']} by {sorted_danceability.iloc[0]['artist']} with danceability = {sorted_danceability.iloc[0]['danceability']}. 
    Least danceable track is {sorted_danceability.iloc[-1]['name']} by {sorted_danceability.iloc[-1]['artist']} with danceability = {sorted_danceability.iloc[-1]['danceability']}. 
    """)

    # note: loudness
    print("Tracks loudness insights.")
    mean_loudness, higher_loudness, sorted_loudness = get_common_stat_data(data=dataframe,column='loudness')
    print(f"""
    Loudness is measured in decibels, and ranges for -60dB to 0dB, whereas 0oB is the loudest.
    Mean loudness of playlist is equal to: {mean_loudness}db.
    Tracks with loudness higher or equal take up to {((higher_loudness*100)/len(dataframe)):.1f}% of playlist.
    The loudest track is {sorted_loudness.iloc[0]['name']} by {sorted_loudness.iloc[0]['artist']} with loudness = {sorted_loudness.iloc[0]['loudness']}. 
    The quietest track is {sorted_loudness.iloc[-1]['name']} by {sorted_loudness.iloc[-1]['artist']} with loudness = {sorted_loudness.iloc[-1]['loudness']}. 
    """)

    def interpret_correlation(correlation_value):
        if correlation_value > 0.7:
            return "Strongly positive correlation"
        elif 0.3 <= correlation_value <= 0.7:
            return "Moderate positive correlation"
        elif -0.3 <= correlation_value <= 0.3:
            return "No significant correlation"
        elif -0.7 <= correlation_value < -0.3:
            return "Moderate negative correlation"
        elif correlation_value < -0.7:
            return "Strongly negative correlation"

    def check_correlations(df: pd.DataFrame):
        results = []

        correlations = {
            'energy_valence': df[['energy', 'valence']].corr(method='pearson'),
            'energy_danceability': df[['energy', 'danceability']].corr(method='pearson'),
            'energy_loudness': df[['energy', 'loudness']].corr(method='pearson'),
            'danceability_valence': df[['danceability', 'valence']].corr(method='pearson'),
            'danceability_loudness': df[['danceability', 'loudness']].corr(method='pearson')
        }

        for key, correlation_matrix in correlations.items():
            correlation_value = correlation_matrix.iloc[0, 1]
            interpretation = interpret_correlation(correlation_value)
            result = f"{key}: {interpretation} ({correlation_value:.2f})"
            results.append(result)

        return results

    corr_results = check_correlations(dataframe)
    print(f"Correlations between different track features:\n")
    for cr in corr_results:
        print("\t" + cr)


    plot_tempo(df=dataframe)
    plot_energy_and_valence(df=dataframe)
    plot_random_tracks_features(df=dataframe)

# done: done: done:
def get_avg_track_duration(dataframe: pd.DataFrame):
    print("Tracks duration insights.\n")

    # means and extremes:
    total_duration = dataframe['duration'].sum()
    mean_duration, higher_duration, sorted_duration = get_common_stat_data(data=dataframe, column='duration')

    # time converts
    longest_min, longest_sec = ms_to_min_converter(sorted_duration.iloc[0]['duration'])
    shortest_min, shortest_sec = ms_to_min_converter(sorted_duration.iloc[-1]['duration'])
    mean_min, mean_secs = ms_to_min_converter(mean_duration)
    tot_min, tot_secs = ms_to_min_converter(total_duration)

    print(f"""
    Total playlist duration = {tot_min}min {tot_secs}s.
    Mean track duration = {mean_min}min {mean_secs}s.
    {(higher_duration*100/len(dataframe)):.0f}% of playlist tracks have equal or longer duration.\n
    Longest song is '{sorted_duration.iloc[0]['name']}' by {sorted_duration.iloc[0]['artist']} with duration = {longest_min}min {longest_sec}s,
    and it takes {((sorted_duration.iloc[0]['duration'] * 100)/ total_duration):.1f}% of whole playlist duration.
    The shortest, on the other hand, is '{sorted_duration.iloc[-1]['name']}' by {sorted_duration.iloc[-1]['artist']} with 
    duration = {shortest_min}min {shortest_sec}s, takes {((sorted_duration.iloc[-1]['duration'] * 100)/ total_duration):.1f}% of whole playlist duration.\n\n
    """)

    pie_duration(sorted_duration)

#done: done: done:
def get_common_release_years_of_tracks(dataframe: pd.DataFrame):
    print("Tracks albums release years insights.\n")

    dataframe['album_release_date'] = pd.to_datetime(dataframe['album_release_date']).dt.date
    sorted_df = dataframe.sort_values(by="album_release_date", ascending=False)
    over_2020 = sorted_df.loc[sorted_df['album_release_date'] >= datetime.date(2020, 1, 1)]

    print(f"""
    About {((len(over_2020)*100)/ len(dataframe)):.1f}% of albums were released after year 2020.\n
    Newest track on the playlist is {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} 
    released on {sorted_df.iloc[0]['album_release_date']}. The oldest track, on the other hand, is {sorted_df.iloc[-1]['name']} 
    by {sorted_df.iloc[-1]['artist']} released on {sorted_df.iloc[-1]['album_release_date']}.\n\n
    """)

    plot_pie_release_years(df=sorted_df)

# done: done: done:
def get_top_playlist_artists_and_words(dataframe: pd.DataFrame):
    print("Artist insights.")

    # counters and extremes:
    artist_count = Counter(dataframe['artist'])

    total_artists = len(dataframe['artist'].drop_duplicates())
    artists_duplicates = sum(count>1 for count in artist_count.values())

    most_common = artist_count.most_common(10)
    artist, count = zip(*most_common)
    overall_min, overall_secs = ms_to_min_converter(dataframe['duration'].sum())

    #time
    one_trackers = [a for a, c in artist_count.items() if c == 1]
    one_trackers_data = dataframe[dataframe['artist'].isin(one_trackers)]
    top_1 = dataframe[dataframe['artist'] == artist[0]]['duration'].sum()
    top_min, top_secs = ms_to_min_converter(top_1)
    one_min, one_secs = ms_to_min_converter(one_trackers_data['duration'].sum())

    #most common words counter
    list_names = [j.lower() for i in [i.split() for i in dataframe['name']] for j in i]
    words_count = Counter()
    for i in list_names:
        if i.isalpha():
            if i in words_count:
                words_count[i] += 1
            else:
                words_count[i] = 1

    print(f"""
    There are {total_artists} distinct and {artists_duplicates} duplicated artists on the playlist.
    Most common artist, {artist[0]}, takes about {((artist_count[artist[0]]*100)/len(dataframe)):.1f}% of all 
    artists and their sum of track duration = {top_min}min {top_secs}s.\n
    About {((len(one_trackers)*100)/len(dataframe)):.1f}% of artists own only one song on the playlist,
    and they owe {one_min}min {one_secs}s in playlist.
    Out of total {overall_min}min {overall_secs}s playlist duration.
    Most common words in titles are: {words_count.most_common(3)}.
    """)

    plot_artists(artists=artist, counts=count)


async def _main():
    load_dotenv()
    user =  os.getenv("USER_ID", None)
    playlist_id = os.getenv("PLAYLIST_ID", None)

    track_df = pd.DataFrame(pd.read_csv("playlists/books.mp3_playlist.csv", sep=";", index_col=0))

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    asyncio.run(main=_main())
