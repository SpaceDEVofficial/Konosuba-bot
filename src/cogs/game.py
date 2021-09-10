import discord
from discord.ext import commands
from utils.create_embed import embeds
from utils.db_tool import DB_tools
import asyncio
class regist(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="스킬")
    async def skill(self,ctx):
        em = embeds().aqua_skill()
        msg = await ctx.reply(embed=em)
        await asyncio.sleep(3.1)
        em = embeds().idle_embed()
        await msg.edit(embed=em)


def setup(bot):
    bot.add_cog(regist(bot))
