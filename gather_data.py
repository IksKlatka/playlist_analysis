import os
import aiohttp
import asyncio
import pandas as pd
from dotenv import load_dotenv

import additional_functions
from models import User, Track, Playlist

base_url = "https://api.spotify.com"

load_dotenv()
headers = {
    "Authorization" : "Bearer " + os.getenv('TOKEN', None)
}

async def get_user_info(user_id: str) -> User:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(base_url+f'/v1/users/{user_id}') as response:
            data = await response.json()
            user = User(id=data['id'], username=data['display_name'])
            return user


async def get_playlist_info(playlist_id: str):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(base_url+f'/v1/playlists/{playlist_id}') as response:
            try:
                data = await additional_functions.validate_response(response)
                # del data['images']
                # for d in data['tracks']['items']:
                #     del d['track']['available_markets']
                #     del d['track']['album']['available_markets']
                #     del d['track']['album']['images']
                return data
            except (TypeError, ValueError) as error:
                print(f"Error occurred while fetching track features: {error}")
                return

async def get_track_features(track_id: str) -> dict:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(base_url+f'/v1/audio-features/{track_id}') as response:
            try:
                data = await additional_functions.validate_response(response)
                return data
            except (TypeError, ValueError) as error:
                print(f"Error occurred while fetching track features: {error}")
                return

# note : hardly ever there are genres
async def get_album_genres(album_id: str):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(base_url + f'/v1/albums/{album_id}') as response:
            try:
                data = await additional_functions.validate_response(response)
                return data
            except (TypeError, ValueError) as error:
                print(f"Error occurred while fetching track features: {error}")
                return


async def get_playlist_items(playlist_id: str, offset: int = 0):
    p_info = await get_playlist_info(playlist_id)
    total_songs = p_info['tracks']['total']

    all_songs = []
    async def fetch_track_data(song):
        audio_data = await get_track_features(song['track']['id'])
        genre_data = await get_album_genres(song['track']['album']['id'])

        track = Track(id=song['track']['id'],
                      name=song['track']['name'],
                      artist=song['track']['artists'][0]['name'],
                      album=song['track']['album']['name'],
                      album_release_date=song['track']['album']['release_date'],
                      duration=song['track']['duration_ms'],
                      valence = audio_data['valence'],
                      energy =  audio_data['energy'],
                      genres= genre_data['genres'])

        return track

    def playlist_info_to_object(playlist: dict, total_duration: int) -> Playlist:

        return Playlist(id=playlist['id'], name=playlist['name'], author=playlist['owner']['display_name'],
                               total_songs=playlist['tracks']['total'], duration=total_duration)

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        while total_songs > 0:
            limit = min(total_songs, 50)
            async with session.get(
                    base_url + f'/v1/playlists/{playlist_id}/tracks?offset={offset}&limit={limit}') as response:
                data = await response.json()
                for song in data['items']:
                    tasks.append(fetch_track_data(song))

                total_songs -= limit
                offset += limit

        tracks = await asyncio.gather(*tasks)
        all_songs.extend(tracks)

    total_duration = 0
    for i, pi in enumerate(all_songs):
        total_duration += pi.duration

    playlist = playlist_info_to_object(p_info, total_duration)

    return all_songs, playlist



async def _main():

    user_id = 'iga.klatka'
    playlist_id = '3VrrnKPss90ctQ4LHiVM0l'

    # user = await get_user_info(user_id)
    # user_df = pd.DataFrame(user)
    # additional_functions.save_to_file(user_df, "user_data")

    playlist_items, playlist_info = await get_playlist_items(playlist_id=playlist_id)

    tracks_df = additional_functions.objects_to_dataframes(playlist_items)
    additional_functions.save_to_file(tracks_df, playlist_info.name+"_playlist")

    # d = await get_track_features("04qez0ficd7e4SdHjkxoMq")
    # print(d)

if __name__ == '__main__':

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_main())

