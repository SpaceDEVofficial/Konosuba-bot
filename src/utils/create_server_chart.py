import os

import discord
from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp
from .db_tool import DB_tools
class genchart:

    def __init__(self,bot):
        self.bot = bot
        self.serurl = "http://144.172.75.157:8888/get?type=image"
        self.voteurl = "http://144.172.75.157:8888/voteget?type=image"
        self.session = aiohttp.ClientSession(loop=self.bot.loop)


    async def get_chart(self):
        async with self.session.get(self.serurl) as response:
            # this gives us our response object, and now we can read the bytes from it.
            chart_bytes = io.BytesIO(await response.read())
            await self.session.close()
            return chart_bytes

    async def GeneratechartCard(self):
        chart = await self.get_chart()
        cht = Image.open(chart)
        bytes = io.BytesIO()
        cht.save(bytes, 'PNG')
        bytes.seek(0)
        return {"type":True,"img":bytes}

    async def get_votechart(self):
        async with self.session.get(self.voteurl) as response:
            # this gives us our response object, and now we can read the bytes from it.
            chart_bytes = io.BytesIO(await response.read())
            await self.session.close()
            return chart_bytes

    async def GeneratevotechartCard(self):
        chart = await self.get_votechart()
        cht = Image.open(chart)
        bytes = io.BytesIO()
        cht.save(bytes, 'PNG')
        bytes.seek(0)
        return {"type":True,"img":bytes}
