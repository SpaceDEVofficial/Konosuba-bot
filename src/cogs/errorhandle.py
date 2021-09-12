from discord.ext import commands

#from src.utils.execption import PermError
from utils.execption import PermError
from src.utils.create_embed import embeds

class handling(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, PermError.NotRegister):
            return await embeds(ctx=ctx).NotRegister()

def setup(bot):
    bot.add_cog(handling(bot))