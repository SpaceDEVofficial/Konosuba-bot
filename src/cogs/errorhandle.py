import traceback

from discord.ext import commands

#from src.utils.execption import PermError
from utils.execption import PermError
from utils.create_embed import embeds

class handling(commands.Cog):
    """
    에러를 처리하는 곳이야
    """
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        print(str(traceback.format_exc()))
        if isinstance(error, PermError.NotRegister):
            return await embeds(ctx=ctx).NotRegister()

def setup(bot):
    bot.add_cog(handling(bot))