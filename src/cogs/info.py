import discord
from discord.ext import commands
from utils.create_embed import embeds
from utils.db_tool import DB_tools
from utils.create_infocard import gencard
import asyncio
class info(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="정보")
    async def info(self,ctx):
        img = await gencard(bot=self.bot,ctx=ctx).GenerateInfoCard()
        await ctx.replt(file=discord.File(fp=img,filename=f'{ctx.author.id}.png'))


def setup(bot):
    bot.add_cog(info(bot))
