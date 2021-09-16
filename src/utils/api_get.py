import json

import aiohttp

async def _request_api(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            read = await res.read()
            sid = read.decode('utf-8')
            answer = json.loads(sid)
            return answer