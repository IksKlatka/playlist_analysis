import asyncio
import os
from dotenv import load_dotenv
import asyncpg


load_dotenv()
credentials = {
    "user" : os.getenv("DB_USER", None),
    "password" : os.getenv("DB_PASSWORD", None),
    "db" : os.getenv("DB_NAME", None),
    "host" : os.getenv("DB_HOST", None)
}


class Database:
    async def initialize_connection(self):
        self.pool = await asyncpg.create_pool(**credentials)

        print("connected!")

    async def get_track_by_id(self):
        pass

    async def insert_track(self):
        pass

    async def delete_track_by_id(self):
        pass


async def _main(): pass


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(_main())