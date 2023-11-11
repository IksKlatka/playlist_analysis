import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

def plot_tempo(df: pd.DataFrame):
    tempo = df['tempo']
    mean = tempo.mean()

    plt.plot(tempo, color="#004e8a", label="Tempo")
    plt.axhline(mean, color="#ff009d", label="Mean Tempo")
    plt.xlabel("Track index")
    plt.ylabel("Tempo (BPS)")
    plt.title("Tempo changes throughout playlist.")
    plt.show()

def plot_energy_and_valence(df: pd.DataFrame):

    df = df.head(24)
    plt.figure(figsize=(14, 6))
    energy_colors = ['#31d115' if v >= 0.75 else ('#005213' if v >= 0.5 and v < 0.75 else '#42950f') for v in df['energy']]
    valence_colors = ['#004e8a' if v >= 0.75 else ('#0b8978' if v >= 0.5 and v < 0.75 else '#147d99') for v in df['valence']]

    plt.subplot(1, 2, 1)
    plt.bar(df['artist'], df['energy'], color=energy_colors)
    plt.ylabel("Energy")
    plt.xlabel("Artist")
    plt.title("Energy levels of first 24 tracks in the playlist.")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.subplot(1, 2, 2)
    plt.bar(df['artist'], df['valence'], color=valence_colors)
    plt.ylabel("Valence")
    plt.xlabel("Artist")
    plt.title("Valence levels of first 24 tracks in the playlist.")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()

def plot_random_tracks_features(df: pd.DataFrame):
    random_tracks = df.sample(8)

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

def pie_duration(df: pd.DataFrame):

    # pie chart preparation
    bins = [0, 180000, 300000, 420000, float('inf')]
    labels = ['<3 min', '3-5 min', '5-7 min', '7+ min']

    df['duration_category'] = pd.cut(df['duration'], bins=bins, labels=labels)
    duration_counts = df['duration_category'].value_counts()

    explodes = [0.02 for _ in range(len(df['duration_category'].value_counts()))]
    plt.figure(figsize=(8, 8))
    plt.pie(duration_counts, labels=duration_counts.index,  autopct='%1.1f%%', startangle=90, explode=explodes)
    plt.title('Distribution of Track Durations in Playlist')
    plt.show()

def plot_pie_release_years(df: pd.DataFrame):

    release_years = Counter([date.year for date in df['album_release_date']])

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

def plot_artists(artists: tuple, counts: tuple):
    # plots
    colors = ['#0cb800' if c > 10 else ('#fb0' if c > 5 else '#ff009d') for c in counts]
    plt.bar(artists, counts, color=colors)

    plt.ylabel("Songs count")
    plt.xlabel("Artists")
    plt.title("10 most common artists in playlist.")

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

