import os
from utils.checks import require
from utils.db_tool import DB_tools
import discord
import koreanbots
import UniqueBotsKR
from discord.ext import commands
from dotenv import load_dotenv
from utils.create_server_chart import genchart
from utils.create_embed import embeds

load_dotenv(verbose=True)

class MyStatcordCog(commands.Cog):
    """
    봇상태를 업데이트하는 그룹이야!
    """
    def __init__(self, bot):
        self.bot = bot
        self.kb = koreanbots.Koreanbots(self.bot, os.getenv("KBTOKEN"), run_task=True)
        self.ub = UniqueBotsKR.client(self.bot, token=os.getenv("UBTOKEN"),autopost=True)

    async def get_heart(self,ctx,id:int,official:bool):
        if official:
            li = []
            quts = 0
            UB = await self.ub.getHeartUser(user_id=id)
            KB = await self.kb.get_user_vote(user_id=id,bot_id=885712681498214450)
            print(f"UB: {UB}")
            print(f"KB: {KB}")
            if UB:
                li.append("UniqueBots: ❤인증완료!")
                await DB_tools(ctx=ctx, bot=self.bot).heart_check_gift()
                quts += 5
            else:
                li.append("UniqueBots: 💔인증실패..[여기](<https://uniquebots.kr/bots/info/885712681498214450>)로 가셔서 하트 눌러주세요!💕")
            if KB['data']['voted']:
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
            if quts == 0:
                ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=em)
        li = []
        quts = 0
        UB = await self.ub.getHeartUser(user_id=id)
        KB = await self.kb.get_user_vote(user_id=id, bot_id=885712681498214450)
        print(f"UB: {UB}")
        print(f"KB: {KB}")
        if UB:
            li.append("UniqueBots: ❤인증완료!")
            quts += 5
        else:
            li.append("UniqueBots: 💔인증실패..[여기](<https://uniquebots.kr/bots/info/885712681498214450>)로 가셔서 하트 눌러주세요!💕")
        if KB['data']['voted']:
            li.append("KoreanBots: ❤인증완료!")
            quts += 5
        else:
            li.append(
                "KoreanBots: 💔인증실패..[여기](<https://koreanbots.dev/bots/885712681498214450/vote>)로 가셔서 하트 눌러주세요!💕")
        em = discord.Embed(
            title=f"{ctx.author}님의 하트여부",
            description="\n".join(li)
        )
        url = "https://discord.gg/Jk6VRvsnqa"
        em.add_field(name="총 보상", value=f"*보상을 받으실려면 공식 서포트채널에서 해주세요.*\n[초대링크](<{url}>)")
        em.set_thumbnail(
            url="https://media.discordapp.net/attachments/885771035243347978/888347900592128030/konosubaLogo.png")
        em.set_footer(text="이 봇은 NEXON에서 서비스하는 봇이 아닙니다.")
        if quts == 0:
            ctx.command.reset_cooldown(ctx)
        return await ctx.reply(embed=em)

    @require()
    @commands.command(name="하트인증",help="각각의 봇 사이트에서 하트를 인증할수있어!")
    @commands.cooldown(1,60*60,commands.BucketType.user)
    async def heart_check(self,ctx):
        if ctx.guild.id != 847729860881154078:
            #ctx.command.reset_cooldown(ctx)
            #return await embeds(ctx=ctx).Not_support_guild()
            return await self.get_heart(ctx=ctx,id=ctx.author.id,official=False)
        await self.get_heart(ctx=ctx,id=ctx.author.id,official=True)

    @commands.command(name="서버차트",help="봇 서버수를 시간별 차트로 보여줘!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def server_chart(self, ctx):
        msg = await ctx.reply("> API서버에 요청하는 중입니다... <a:loading:888625946565935167>")
        img = await genchart(bot=self.bot).GeneratechartCard()
        if img["type"]:
            msg2 = await msg.edit(content="> 이미지 생성완료! 임베드 전송중... <a:loading:888625946565935167>")
            await msg2.delete()
            await embeds(ctx=ctx).chart_embed(img=img["img"], img_name='output.png', url="attachment://output.png")

    @commands.command(name="하트차트", help="봇 서버수를 시간별 차트로 보여줘!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vote_chart(self, ctx):
        msg = await ctx.reply("> API서버에 요청하는 중입니다... <a:loading:888625946565935167>")
        img = await genchart(bot=self.bot).GeneratevotechartCard()
        if img["type"]:
            msg2 = await msg.edit(content="> 이미지 생성완료! 임베드 전송중... <a:loading:888625946565935167>")
            await msg2.delete()
            await embeds(ctx=ctx).vote_chart_embed(img=img["img"], img_name='output.png', url="attachment://output.png")

def setup(bot):
    bot.add_cog(MyStatcordCog(bot))
