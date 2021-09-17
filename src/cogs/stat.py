import os

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
        UB = await self.ub.getHeart(id)
        KB = await self.kb.get_user_vote(user_id=id,bot_id=885712681498214450)
        if UB:
            li.append("UniqueBots: ❤인증완료!")
        else:
            li.append("UniqueBots: 💔인증실패..[여기](<https://uniquebots.kr/bots/info/885712681498214450>)로 가셔서 하트 눌러주세요!💕")
        if KB:
            li.append("KoreanBots: ❤인증완료!")
        else:
            li.append("KoreanBots: 💔인증실패..[여기](<https://koreanbots.dev/bots/885712681498214450/vote>)로 가셔서 하트 눌러주세요!💕")
        em = discord.Embed(
            title=f"{ctx.author}님의 하트여부",
            description="\n".join(li)
        )

    @commands.command(name="하트인증",help="각각의 봇 사이트에서 하트를 인증할수있어!")
    async def heart_check(self,ctx):


def setup(bot):
    bot.add_cog(MyStatcordCog(bot))
