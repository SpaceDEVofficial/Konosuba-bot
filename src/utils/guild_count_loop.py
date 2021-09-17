import datetime
import time

from async_task_helpers import loop
import aiohttp
import asyncio
import aiosqlite

async def loops():
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://koreanbots.dev/api/v2/bots/885712681498214450") as res:
            re = await res.json()
            servs = re["data"]["servers"]
            date = datetime.datetime.now()
            date_text = f"{date.year}/{date.month}/{date.day} {date.hour}:{date.minute}"
            async with aiosqlite.connect("db/db.db") as con:
                await con.execute("INSERT INTO guild_count VALUES (?,?)",(date_text,servs))
                await con.commit()
            print(f"Updated. Servers: {servs}")
    await asyncio.sleep(60*10)

async def main():
    task = await asyncio.create_task(loops())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
loop.run_until_complete(main())