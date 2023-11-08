import asyncio

from additional_functions import extract_playlist_id, objects_to_dataframes, save_to_file
import gather_data
import analysis


async def _main():

    print("""This project will show you some insights of your Spotify playlist.")
    In order to gather them, I need link to Spotify playlist.
    """)

    playlist_link = input("Paste the link here:  ")
    playlist_id = await extract_playlist_id(playlist_link)

    if playlist_id is None:
        raise ValueError("Playlist id is None.")
        return

    playlist_items, playlist_info = await gather_data.get_playlist_items(playlist_id)
    track_df = objects_to_dataframes(playlist_items)
    save_to_file(track_df, playlist_info.name)

    print(f"So, first of all, let's check facts, {playlist_info.author}: ")

    if input(f"Is your playlist name {playlist_info.name}?").lower() == "y":
        print(f"Great. So here's your interesting data about playlist '{playlist_info.name}':")
    else:
        print("Whoa, not good.")
        exit()

    await analysis.get_top_playlist_artists(track_df)
    await analysis.get_avg_track_duration(track_df)
    await analysis.get_avg_playlist_valence(track_df)
    await analysis.get_avg_playlist_energy(track_df)
    await analysis.get_common_release_years_of_tracks(track_df)

    print(f"I hope you enjoyed this, {playlist_info.author}. Nice playlist!")



if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_main())