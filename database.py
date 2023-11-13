import asyncio
import os
from asyncio import create_task

import pandas as pd
from dotenv import load_dotenv
import asyncpg

import additional_functions
from models import Track

load_dotenv()
credentials = {
    "user" : os.getenv("DB_USER", None),
    "password" : os.getenv("DB_PASSWORD", None),
    "database" : os.getenv("DB_NAME", None),
    "host" : os.getenv("DB_HOST", None)
}


class Database:
    async def initialize_connection(self):
        self.pool = await asyncpg.create_pool(**credentials)

        print("connected!")

    async def get_const_track_by_id(self, track_id: str) -> Track:
        async with self.pool.acquire() as connection:
            track = await connection.fetchrow("SELECT * FROM const_tracks WHERE track_id = $1",
                                              track_id)
            if track:
                return track
            else:
                return None
    async def insert_track_without_pid(self, track: Track):
        async with self.pool.acquire() as connection:
            exists = await self.get_const_track_by_id(track.id)
            if exists is None:
                new = await connection.fetchrow("""
                INSERT INTO const_tracks(track_id, name, artist, album, album_release_date, 
                duration, valence, energy, tempo, loudness, danceability) VALUES 
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                """, track.id, track.name, track.artist, track.album, track.album_release_date, track.duration,
                                track.valence, track.energy, track.tempo, track.loudness, track.danceability)
            else:
                raise ValueError(f"Track with id={track.id} is present in database.")

            return 1

    async def insert_track_with_pid(self, track: Track):
        async with self.pool.acquire() as connection:
            exists = await self.get_const_track_by_id(track.id)
            if exists is None:
                new = await connection.fetchrow("""
                INSERT INTO const_tracks(playlist_id, track_id, name, artist, album, album_release_date, 
                duration, valence, energy, tempo, loudness, danceability) VALUES 
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)""",
                     track.playlist_id, track.id, track.name, track.artist, track.album, track.album_release_date,
                     track.duration, track.valence, track.energy, track.tempo, track.loudness, track.danceability)
            else:
                raise ValueError(f"Track with id={track.id} is present in database.")

            return 1

    async def delete_temp_track_by_playlist_id(self, playlist_id):
        async with self.pool.acquire() as connection:
            await connection.fetchrow("DELETE FROM const_tracks WHERE playlist_id = $1", playlist_id)
            return f"Deleted tracks with {playlist_id=}"


async def _main():
    db = Database()
    await db.initialize_connection()

    tracks = pd.DataFrame(pd.read_csv("playlists/X.ar.csv", sep=';', index_col=0))
    all_tracks = additional_functions.dataframe_to_objects(tracks)
    for i, track in enumerate(all_tracks):
        try:
            await db.insert_track_without_pid(track)
        except ValueError:
            continue
        if i % 100 == 0:
            print(f"done in {i*100/len(all_tracks):.1f}%")

    print("all done")

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_main())