import os
from utils.checks import require
from utils.db_tool import DB_tools
import discord
import koreanbots
import UniqueBotsKR
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv(verbose=True)

class MyStatcordCog(commands.Cog):
    """
    봇상태를 업데이트하는 그룹이야!
    """
    def __init__(self, bot):
        self.bot = bot
        self.kb = koreanbots.Koreanbots(self.bot, os.getenv("KBTOKEN"), run_task=True)
        self.ub = UniqueBotsKR.client(self.bot, token=os.getenv("UBTOKEN"),autopost=True)

    async def get_heart(self,ctx,id:int):
        li = []
        quts = 0
        UB = await self.ub.getHeartUser(user_id=id)
        KB = await self.kb.get_user_vote(user_id=id,bot_id=885712681498214450)
        if UB:
            li.append("UniqueBots: ❤인증완료!")
            await DB_tools(ctx=ctx, bot=self.bot).heart_check_gift()
            quts += 5
        else:
            li.append("UniqueBots: 💔인증실패..[여기](<https://uniquebots.kr/bots/info/885712681498214450>)로 가셔서 하트 눌러주세요!💕")
        if KB:
            li.append("KoreanBots: ❤인증완료!")
            await DB_tools(ctx=ctx, bot=self.bot).heart_check_gift()
            quts += 5
        else:
            li.append("KoreanBots: 💔인증실패..[여기](<https://koreanbots.dev/bots/885712681498214450/vote>)로 가셔서 하트 눌러주세요!💕")
        em = discord.Embed(
            title=f"{ctx.author}님의 하트여부",
            description="\n".join(li)
        )
        em.add_field(name="총 보상",value=f"총 `{quts}`개의 쿼츠를 드렸습니다!")
        em.set_thumbnail(url="https://media.discordapp.net/attachments/885771035243347978/888347900592128030/konosubaLogo.png")
        await ctx.reply(embed=em)

    @require()
    @commands.command(name="하트인증",help="각각의 봇 사이트에서 하트를 인증할수있어!")
    @commands.cooldown(1,60*60,commands.BucketType.user)
    async def heart_check(self,ctx):
        await self.get_heart(ctx=ctx,id=ctx.author.id)


def setup(bot):
    bot.add_cog(MyStatcordCog(bot))
