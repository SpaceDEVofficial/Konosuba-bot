import discord
from discord.ext import commands
from utils.create_embed import embeds
from utils.db_tool import DB_tools
from utils.checks import require


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

    @require()
    @commands.command(name="탈퇴")
    async def unregist(self, ctx):
        res = await DB_tools(ctx=ctx, bot=self.bot).unregist()
        if res:
            em = embeds().unregist_ok()
            await ctx.reply(embed=em)
            return
        em = embeds().unregist_no()
        await ctx.reply(embed=em)

    @commands.command(name="hellothisisverification")
    async def hellothisisverification(self,ctx):
        await ctx.send("gawi#9537(281566165699002379)\ngawi#8844(300535826088067072)")


def setup(bot):
    bot.add_cog(regist(bot))
