import os
import aiohttp
import asyncio
from dotenv import load_dotenv
import platform
import base64

load_dotenv()
token = os.getenv("TOKEN", None)
client_id = os.getenv("CLIENT_ID", None)
client_secret = os.getenv("CLIENT_SECRET", None)
refresh_token = os.getenv("REFRESH_TOKEN", None)

base_url = "https://accounts.spotify.com/api/token"

auth_str = client_id + ":" + client_secret
auth_base64 = str(base64.b64encode(auth_str.encode("utf-8")), "utf-8")

headers= {
        "Authorization": 'Basic '+ auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
}

payload = {
    "grant_type" : "client_credentials",
}

def override_token(new_token: str):
    with open('.env', 'r') as file:
        lines = file.readlines()
    t_line = None
    for i, line in enumerate(lines):
        if line.startswith("TOKEN"):
            t_line = i
            break
    if t_line is not None:
        lines[t_line] = f"TOKEN = {new_token}\n"
    with open('.env', 'w') as file:
        file.writelines(lines)

async def get_token():
    async with aiohttp.ClientSession(headers=headers) as Session:
        async with Session.post(url=base_url, data=payload) as response:
            data = await response.json()
            override_token(data['access_token'])


if platform.system()=="Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(get_token())
