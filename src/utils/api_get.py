import aiohttp

async def _request_api(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            read = await res.read()
            return read