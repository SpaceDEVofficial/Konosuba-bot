import datetime
import time
from discord.ext import tasks
import aiohttp
import asyncio
import aiosqlite

sql_create_initial_thunder_table = """ CREATE TABLE IF NOT EXISTS guild_count (

                                    counts integer,

                                    dates text DEFAULT (datetime('now','localtime'))

                                ); """

vote_table = """ CREATE TABLE IF NOT EXISTS vote_count (

                                    counts integer,

                                    dates text DEFAULT (datetime('now','localtime'))

                                ); """

@tasks.loop(minutes=10)
async def loops():
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://koreanbots.dev/api/v2/bots/885712681498214450") as res:
            re = await res.json()
            servs = re["data"]["servers"]
            #date = datetime.datetime.now()
            #date_text = f"{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}"
            async with aiosqlite.connect("db/db.db") as con:
                await con.execute(sql_create_initial_thunder_table)
                await con.execute(f"INSERT INTO guild_count(counts) VALUES (?)",(servs,))
                await con.commit()
            print(f"Updated. Servers: {servs}")
@tasks.loop(minutes=10)
async def vote_loops():
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://koreanbots.dev/api/v2/bots/885712681498214450") as res:
            re = await res.json()
            servs = re["data"]["votes"]
            #date = datetime.datetime.now()
            #date_text = f"{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}"
            async with aiosqlite.connect("db/db.db") as con:
                await con.execute(vote_table)
                await con.execute(f"INSERT INTO vote_count(counts) VALUES (?)",(servs,))
                await con.commit()
            print(f"Updated. votes: {servs}")

loops.start()
vote_loops.start()

asyncio.get_event_loop().run_forever()