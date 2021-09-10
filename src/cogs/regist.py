import discord
from discord.ext import commands
from utils.create_embed import embeds
from utils.db_tool import DB_tools
class regist(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="가입")
    async def regist(self,ctx):
        res = await DB_tools(ctx=ctx,bot=self.bot).regist()
        if res:
            em = embeds().regist_ok()
            await ctx.reply(embed=em)
            return
        em = embeds().regist_no()
        await ctx.reply(embed=em)

    @commands.command(name="탈퇴")
    async def unregist(self, ctx):
        res = await DB_tools(ctx=ctx, bot=self.bot).unregist()
        if res:
            em = embeds().unregist_ok()
            await ctx.reply(embed=em)
            return
        em = embeds().unregist_no()
        await ctx.reply(embed=em)


def setup(bot):
    bot.add_cog(regist(bot))
