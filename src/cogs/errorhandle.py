import traceback

import discord
from discord.ext import commands

#from src.utils.execption import PermError
from utils.execption import PermError
from utils.create_embed import embeds
from data import colors
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
            return await ctx.reply(f"`{ctx.invoked_with}`?")
        elif isinstance(error, commands.errors.PrivateMessageOnly):
            await ctx.send(
                embed=discord.Embed(
                    title='⛔ DM 전용 명령어',
                    description='이 명령어는 개인 메시지에서만 사용할 수 있습니다!',
                    color=colors.ERROR
                )
            )

        elif isinstance(error, commands.NotOwner):
            await ctx.send(
                embed=discord.Embed(
                    title='⛔ 개발자 전용 명령어',
                    description='이 명령어는 개발자만 사용할 수 있습니다.',
                    color=colors.ERROR
                )
            )
        else:
            tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            print(tb)
            await ctx.send(
                embed=discord.Embed(
                    title="❌ 오류가 발생했습니다!",
                    description=f'```python\n{tb}```',
                    color=colors.ERROR
                )
            )

def setup(bot):
    bot.add_cog(handling(bot))