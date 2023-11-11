import asyncio
import datetime
import pandas as pd
from collections import Counter
import additional_functions
import matplotlib.pyplot as plt
import seaborn as sns
import string

from additional_functions import ms_to_min_converter

def objects_to_dataframes(objects) -> pd.DataFrame:
    if isinstance(objects, list):
        return pd.DataFrame.from_records([o.__dict__ for o in objects])
    else:
        raise TypeError("The 'objects' argument should be a list of class instances.")

# done:
def get_track_features_data(dataframe: pd.DataFrame):
    """
    Insights of tracks features such as:
    - tempo, - energy, - valence, - danceability, - loudness
    returning information about means, correlation, extremes,
    """
    #todo:
    # separate plotting from analysis
    # done: multi-bar plot with N random tracks ands their features values

    if len(dataframe) > 25:
        print("Because of size of the playlist, graph visualizations won't cover all of the tracks.\n")

    def levels(mean_energy):
        if mean_energy <= 0.25:
            return "very low"
        elif mean_energy > 0.25 and mean_energy <= 0.5:
            return "low"
        elif mean_energy > 0.5 and mean_energy <= 0.75:
            return "moderate"
        else:
            return "high"

    #note: tempo ------------------------------------------------------

    tempo = dataframe['tempo']
    mean = tempo.mean()

    plt.plot(tempo, color="#004e8a", label="Tempo")
    plt.axhline(mean, color="#ff009d", label="Mean Tempo")
    plt.xlabel("Track index")
    plt.ylabel("Tempo (BPS)")
    plt.title("Tempo changes throughout playlist.")
    plt.show()


    #note: energy ------------------------------------------------------
    print("Tracks energy insights.")
    mean_energy = round(dataframe['energy'].mean(), 3)



    sorted_df = dataframe.sort_values(by='energy', ascending=False)
    more_energy = len(dataframe.loc[dataframe['energy'] >= mean_energy])
    first_24 = dataframe.head(24)

    print(f"""
    Mean energy of this playlist is {mean_energy}, which is {levels(mean_energy)} energy.
    About {((more_energy*100)/len(dataframe)):.1f}% of tracks have higher or equal energy level to mean value.
    The most energetic song in playlist is: {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} with energy = {sorted_df.iloc[0]['energy']}
    The least energetic song in playlist is: {sorted_df.iloc[-1]['name']} by {sorted_df.iloc[-1]['artist']} with energy = {sorted_df.iloc[-1]['energy']}
    """)

    colors = ['#004e8a' if v >= 0.75 else ('#0b8978' if v >= 0.5 and v < 0.75 else '#147d99') for v in first_24['energy']]
    plt.figure(figsize=(7, 6))
    plt.bar(first_24['artist'], first_24['energy'], color=colors)
    plt.ylabel("Energy")
    plt.xlabel("Artist")
    plt.title("Energy levels of first 24 tracks in the playlist.")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # note: valence ---------------------------------------------
    print("Tracks mood insights.")
    mean_valence = round(dataframe['valence'].mean(), 3)
    more_positive = len(dataframe.loc[dataframe['valence'] > mean_valence])
    sorted_df = dataframe.sort_values(by='valence', ascending=False)


    print(f"""
    Mean positiveness of this playlist is equal to: {mean_valence}, which is {levels(mean_valence)} valence.
    About {((more_positive*100)/len(dataframe)):.1f}% of tracks have higher valence than the mean value.
    Most positive track on the playlist is {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} with valence = {sorted_df.iloc[0]['valence']}.
    Most depressive track on the playlist is {sorted_df.iloc[-1]['name']} by {sorted_df.iloc[-1]['artist']} with valence = {sorted_df.iloc[-1]['valence']}.\n
    """)
    first_24 = sorted_df.head(24)

    colors = ['#004e8a' if v >= 0.75 else ('#0b8978' if v >= 0.5 and v < 0.75 else '#147d99') for v in first_24['valence']]
    plt.figure(figsize=(7, 6))
    plt.bar(first_24['artist'], first_24['valence'], color=colors)
    plt.ylabel("Valence")
    plt.xlabel("Artist")
    plt.title("Valence levels of first 24 tracks in the playlist.")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


    # note: danceability ----------------------------------------------
    print("Tracks danceability insights.")

    mean_danceability = round(dataframe['danceability'].mean(), 3)
    more_danceable = len(dataframe.loc[dataframe['danceability'] >= mean_danceability])
    sorted_df = dataframe.sort_values(by='danceability', ascending=False)

    print(f"""
    Mean danceability of playlist is equal to: {mean_danceability}, which is {levels(mean_danceability)} danceability.
    Tracks with danceability higher or equal take up to {((more_danceable*100)/len(dataframe)):.1f}% of playlist.
    Most danceable track is {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} with danceability = {sorted_df.iloc[0]['danceability']}. 
    Least danceable track is {sorted_df.iloc[-1]['name']} by {sorted_df.iloc[-1]['artist']} with danceability = {sorted_df.iloc[-1]['danceability']}. 
    """)

    # note: loudness --------------------------------------------------
    print("Tracks loudness insights.")

    mean_loudness = round(dataframe['loudness'].mean(), 3)
    more_loud = len(dataframe.loc[dataframe['loudness'] >= mean_loudness])
    sorted_df = dataframe.sort_values(by='loudness', ascending=False)

    print(f"""
    Loudness is measured in decibels, and ranges for -60dB to 0dB, whereas 0oB is the loudest.
    Mean loudness of playlist is equal to: {mean_loudness}db.
    Tracks with loudness higher or equal take up to {((more_loud*100)/len(dataframe)):.1f}% of playlist.
    The loudest track is {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} with loudness = {sorted_df.iloc[0]['loudness']}. 
    The quietest track is {sorted_df.iloc[-1]['name']} by {sorted_df.iloc[-1]['artist']} with loudness = {sorted_df.iloc[-1]['loudness']}. 
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

    random_tracks = dataframe.sample(8)

    random_tracks_df = random_tracks[['name', 'danceability', 'energy', 'valence']]
    melted = pd.melt(random_tracks_df, id_vars="name", var_name="metrics", value_name="value")
    colors = {'danceability': '#c700d1', 'energy': '#fb0', 'valence': '#2989ff'}
    sns.barplot(x="name", y="value", hue="metrics", data=melted, palette=colors)
    plt.title("8 random tracks features.")
    plt.xlabel("name")
    plt.ylabel("value level")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# done:
def get_avg_track_duration(dataframe: pd.DataFrame):
    print("Tracks duration insights.\n")

    # means and extremes:
    total_duration = dataframe['duration'].sum()
    mean_track_duration = dataframe['duration'].mean()
    short_tracks = len(dataframe.loc[dataframe['duration'] < mean_track_duration])
    sorted_df = dataframe.sort_values(by='duration', ascending=False)
    longest_track = sorted_df.iloc[0]['name']
    shortest_track = sorted_df.iloc[-1]['name']

    # time converts
    longest_min, longest_sec = ms_to_min_converter(sorted_df.iloc[0]['duration'])
    shortest_min, shortest_sec = ms_to_min_converter(sorted_df.iloc[-1]['duration'])
    mean_min, mean_secs = ms_to_min_converter(mean_track_duration)
    tot_min, tot_secs = ms_to_min_converter(total_duration)

    # pie chart preparation
    bins = [0, 180000, 300000, 420000, float('inf')]
    labels = ['<3 min', '3-5 min', '5-7 min', '7+ min']

    sorted_df['duration_category'] = pd.cut(sorted_df['duration'], bins=bins, labels=labels)
    duration_counts = sorted_df['duration_category'].value_counts()

    print(f"""
    Total playlist duration = {tot_min}min {tot_secs}s.
    Mean track duration = {mean_min}min {mean_secs}s.
    Which is longer than {(short_tracks*100/len(dataframe)):.0f}% of playlist songs.\n
    Longest song is '{longest_track}' by {sorted_df.iloc[0]['artist']} with duration = {longest_min}min {longest_sec}s,
    and it takes {((sorted_df.iloc[0]['duration'] * 100)/ total_duration):.1f}% of whole playlist duration.
    The shortest, on the other hand, is '{shortest_track}' by {sorted_df.iloc[-1]['artist']} with 
    duration = {shortest_min}min {shortest_sec}s, takes {((sorted_df.iloc[-1]['duration'] * 100)/ total_duration):.1f}% of whole playlist duration.\n\n
    """)

    explodes = [0.02 for _ in range(len(sorted_df['duration_category'].value_counts()))]
    plt.figure(figsize=(8, 8))
    plt.pie(duration_counts, labels=duration_counts.index,  autopct='%1.1f%%', startangle=90, explode=explodes)
    plt.title('Distribution of Track Durations in Playlist')
    plt.show()

# done:
def get_common_release_years_of_tracks(dataframe: pd.DataFrame):
    print("Tracks albums release years insights.\n")

    dataframe['album_release_date'] = pd.to_datetime(dataframe['album_release_date']).dt.date
    sorted_df = dataframe.sort_values(by="album_release_date", ascending=False)
    release_years = Counter([date.year for date in sorted_df['album_release_date']])
    over_2020 = sorted_df.loc[sorted_df['album_release_date'] >= datetime.date(2020, 1, 1)]

    print(f"""
    About {((len(over_2020)*100)/ len(dataframe)):.1f}% of albums were released after year 2020.\n
    Newest track on the playlist is {sorted_df.iloc[0]['name']} by {sorted_df.iloc[0]['artist']} 
    released on {sorted_df.iloc[0]['album_release_date']}. The oldest track, on the other hand, is {sorted_df.iloc[-1]['name']} 
    by {sorted_df.iloc[-1]['artist']} released on {sorted_df.iloc[-1]['album_release_date']}.\n\n
    """)

    # charts
    grouped_years = Counter()
    for key, value in release_years.items():
        if key >= 2020:
            grouped_years['>= 2020'] += release_years[key]
        elif key >= 2010:
            grouped_years['>= 2010'] += release_years[key]
        else:
            grouped_years['< 2010'] += release_years[key]

    # bar plot -- track counts by years
    colors = ['#bf0' if v >= 20 else ('#fb0' if v >= 10 else '#f70') for v in release_years.values()]

    plt.bar(release_years.keys(), release_years.values(), color=colors)
    plt.xlabel("Years")
    plt.ylabel("Released tracks count.")
    plt.title("Tracks count by release years.")
    plt.xticks(list(map(int, release_years.keys())), rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # pie chart -- grouped by years
    plt.pie(grouped_years.values(), labels=grouped_years.keys(),
            autopct="%1.1f%%", startangle=90, explode=[0.02 for _ in range(len(grouped_years))], colors=['#1f0','#ff8c00', '#f06'])

    plt.title("Tracks count grouped by years.")
    plt.tight_layout()
    plt.show()

# done:
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

    # plots
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

    track_df = pd.DataFrame(pd.read_csv("playlists/books.mp3_playlist.csv", sep=";", index_col=0))
    # get_avg_playlist_energy_valence(track_df)
    get_track_features_data(track_df)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    asyncio.run(main=_main())
