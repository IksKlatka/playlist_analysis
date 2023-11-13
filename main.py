import asyncio
import time
import os
from asyncio import gather, run, create_task

import models
from database import Database
from additional_functions import extract_playlist_id, objects_to_dataframes, save_to_file
import gather_data
import analysis
import os

async def _main():

    print("""This project will show you some insights of your Spotify playlist.")
    In order to gather them, I need the link.
    """)

    playlist_link = input("Paste the link here:  ")
    playlist_id = await extract_playlist_id(playlist_link)

    if playlist_id is None:
        raise ValueError("Playlist id is None.")

    playlist_items, playlist_info = await gather_data.get_playlist_items(playlist_id)
    track_df = objects_to_dataframes(playlist_items)
    save_to_file(track_df, playlist_info.name)

    print(f"So, first of all, let's check facts, {playlist_info.author}: ")

    if input(f"Is your playlist name {playlist_info.name}?").lower() == "y":
        print(f"Great. So here's your interesting data about playlist '{playlist_info.name}':")
    else:
        print("Whoa, not good.")
        exit()

    analysis.get_top_playlist_artists_and_words(track_df)
    analysis.get_avg_track_duration(track_df)
    analysis.get_track_features_data(track_df)
    analysis.get_common_release_years_of_tracks(track_df)

    time.sleep(5)
    print("""
    We've got a question about your data. 
    Would you mind sharing your playlist and tracks data to help us grow?
    You can choose whether to give us: 
    1. your tracks data + playlist ID
    2. only your tracks data
    3. nothing at all. """)
    answer = int(input("\tThe choice is yours (1/2/3): "))

    if answer == 1: await insert_tracks_delete_file(playlist_items, playlist_info)
    if answer == 2: await insert_tracks_delete_file(playlist_items, playlist_info, True)
    else: await del_file(playlist_info.name)
    print("Okay, thanks!")

async def insert_tracks_delete_file(items: list[models.Track], p_info, with_id: bool = False):
    db = Database()
    await db.initialize_connection()

    print(f"All tracks: {len(items)}. Start import.")
    for i, track in enumerate(items):
        if with_id == True:
            try: await db.insert_track_with_pid(track)
            except ValueError: continue
        else:
            try: await db.insert_track_without_pid(track)
            except ValueError: continue
        if i % 100 == 0:
            print(f"import done in {(i * 100)/len(items):.1f}%")
    print("Import finished.")

    await del_file(p_info.name)
    print(f"File deleted.")

async def del_file(playlist_name):
    if os.path.exists(f"playlists/{playlist_name}_playlist.csv"):
        os.remove(f"playlists/{playlist_name}_playlist.csv")
    else:
        print("File does not exist.")


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_main())