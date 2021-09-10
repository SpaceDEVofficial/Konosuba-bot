import discord
from discord.ext import commands
from utils.create_embed import embeds
from utils.db_tool import DB_tools
import asyncio
class info(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="")


def setup(bot):
    bot.add_cog(info(bot))
