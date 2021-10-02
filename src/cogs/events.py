import discord
from discord.ext import commands
import asyncio
from utils.basecog import BaseCog
from utils.rchatmgr import MatchItem
from data import colors
import traceback
from typing import List

class Events(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        bot.event(self.on_message)


    async def on_message(self, message: discord.Message):
        if isinstance(message.channel, discord.DMChannel) and self.rmgr.is_matched(message.author.id) and message.content[3:] not in ['나가기', '참여자']:
            match: List[MatchItem] = self.rmgr.get_matched(message.author.id)
            mymatch = next((m for m in match if m.uid == message.author.id), None)
            match.remove(mymatch)

            await asyncio.gather(
                *(one.send('**[{}]** {}'.format(mymatch.altnick or message.author, message.content)) for one in map(self.bot.get_user, map(lambda x: x.uid, match))),
                return_exceptions=True
            )
        
        else:
            await self.bot.process_commands(message)

        
def setup(bot):
    cog = Events(bot)
    bot.add_cog(cog)