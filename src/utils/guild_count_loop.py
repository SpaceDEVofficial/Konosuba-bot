import datetime

from async_task_helpers import loop
import aiohttp
import asyncio
import aiosqlite


@loop(minutes=5, seconds=30)
async def loop_example():
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://koreanbots.dev/api/v2/bots/885712681498214450") as res:
            re = await res.json()
            servs = re["data"]["servers"]
            date = datetime.datetime.now()
            date_text = f"{date.year}/{date.month}/{date.date} {date.hour}:{date.minute}"
            async with aiosqlite.connect("db/db.db") as con:
                await con.execute("INSERT INTO guild_count VALUES (?,?)",(date_text,servs))
                await con.commit()
                await con.close()
            print(f"Updated. Servers: {servs}")

def start_loop():
    loop_example.start()
asyncio.get_event_loop().run_forever()