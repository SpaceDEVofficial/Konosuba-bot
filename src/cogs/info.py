import io

import discord
from discord.ext import commands
from utils.create_embed import embeds
from utils.db_tool import DB_tools
from utils.create_infocard import gencard
import asyncio
from utils.checks import require
from utils.get_notice import notice
class info(commands.Cog):
    """
    정보관련을 처리하는 그룹이야
    """
    def __init__(self,bot):
        self.bot = bot

    @require()
    @commands.command(name="정보",help="너의 정보를 확인해볼 수 있어!")
    async def info(self,ctx):
        img = await gencard(bot=self.bot,ctx=ctx).GenerateInfoCard()
        if img["type"]:
            await embeds(ctx=ctx).info_embed(img=img["img"],img_name='output.png',url="attachment://output.png")

    @commands.command(name="공지사항",help="코노스바 공식 포럼에 올라와있는 공지사항을 확인해볼 수 있어!")
    async def forum_notice(self,ctx):
        resp = await notice()._get_notice()
        print(resp)
        await embeds(ctx=ctx).send_notice_embed(content=resp)


def setup(bot):
    bot.add_cog(info(bot))
