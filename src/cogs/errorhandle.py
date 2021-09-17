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
        elif isinstance(error,commands.CommandOnCooldown):
            return await ctx.reply(f"마력이 다 회복되려면 `{round(error.retry_after, 2)}`초 남았어요..")
        elif isinstance(error,commands.CommandNotFound):
            return await ctx.reply(f"`{ctx.command.name}`?")

def setup(bot):
    bot.add_cog(handling(bot))