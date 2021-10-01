import html
import io
import json
import re
import traceback
from bs4 import BeautifulSoup
import aiohttp
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
        self.threaddic = {
            "907":"",
            "991":"",
            "982":"",
            "981":"",
            "908":"",
            "912":"",
            "913":""
        }
        self.boardname = {
            "907": "공지사항",
            "991": "업데이트노트",
            "982": "업데이트노트 - 상품",
            "981": "업데이트노트 - 뽑기",
            "908": "이세계 소식통",
            "912": "진행중 이벤트",
            "913": "결과/당첨 발표"
        }
        self.notice = self.bot.loop.create_task(self.notice_loop())
        self.boardid = ["907","991","982","981","908","912","913"]
        #self.notice = None
        #self.updatenote = None
        #self.updatenote_goods = None
        #self.updatenote_gatcha = None
        #self.isakai = None
        #self.event_running = None
        #self.event_result = None
        # Notice = 907
        # updatenote = 991
        # updatenote - goods = 982
        # updatenote - gatcha = 981
        # isakai = 908
        # event = 912
        # event - result = 913


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

    async def update_threadid(self):
        try:
            for i in self.boardid:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://forum.nexon.com/api/v1/board/"+i+"/stickyThreads") as resp:
                        read = await resp.read()
                        sid = read.decode('utf-8')
                        answer = json.loads(sid)
                        self.threaddic[i] = answer['stickyThreads'][0]["threadId"]
            return {"type":True,"msg":"pass"}
        except:
            {"type": False, "msg": str(traceback.format_exc())}

    async def check_update(self):
        try:
            for i in self.boardid:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://forum.nexon.com/api/v1/board/" + i + "/stickyThreads") as resp:
                        read = await resp.read()
                        sid = read.decode('utf-8')
                        answer = json.loads(sid)
                        #self.threaddic[i] = answer['stickyThreads'][0]["threadId"]
                        old_threadid = self.threaddic[i]
                        new_threadid = answer['stickyThreads'][0]["threadId"]
                        if new_threadid != old_threadid:
                            return {"error":False,"content":answer,"boardname":self.boardname[i]}
                        return {"error": False, "content": None}
        except:
            return {"error": True, "content": str(traceback.format_exc())}

    def embed_notice(self,content,boardid,title):
        try:
            first = content['content'].replace("<br>","\n")
            cleanr =re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', first)
            final = html.unescape(cleantext)
            if len(final) >= 1500:
                description = str(final)[:1500] + "..."
            else:
                description = str(final)
            em = discord.Embed(
                title="Nexon 코노스바 모바일 공식포럼 `{boardname}`게시판 업데이트!".format(boardname=self.boardname[boardid]),
                description="글제목: "+title +"\n\n" +description
            )
            soup = BeautifulSoup(content, 'html.parser')

            # find all images
            all_imgs = soup.find_all('img', src=True)
            if not len(all_imgs) == 1:
                num = 0
                for i in all_imgs:
                    num += 1
                    em.add_field(name="** **",value=f"[본문 이미지 #{num}]({i['src']})")
            em.set_image(url=all_imgs[0]['src'])
            em.set_thumbnail(url=content["thumbnailImageUrl"])
            return {"error":False,"embed":em,"error_msg":None}
        except:
            return {"error": True, "embed": None, "error_msg": str(traceback.format_exc())}

    async def notice_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            #res = await self.check_update()
            try:
                for i in self.boardid:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("https://forum.nexon.com/api/v1/board/" + i + "/stickyThreads") as resp:
                            read = await resp.read()
                            sid = read.decode('utf-8')
                            answer = json.loads(sid)
                            # self.threaddic[i] = answer['stickyThreads'][0]["threadId"]
                            old_threadid = self.threaddic[i]
                            new_threadid = answer['stickyThreads'][0]["threadId"]
                            if old_threadid != "" and new_threadid != old_threadid:
                                embed = self.embed_notice(content=answer["content"],
                                                          boardid=answer['stickyThreads'][0]["boardId"],
                                                          title=answer["title"])
                                if not embed["error"]:
                                    embed = embed["embed"]
                                    guilds = self.bot.guilds
                                    ok = []
                                    success = 0
                                    failed = 0
                                    for guild in guilds:
                                        channels = guild.text_channels
                                        for channel in channels:
                                            if guild.id == 653083797763522580 or guild.id == 786470326732587008:
                                                break
                                            if channel.topic is not None:
                                                if str(channel.topic).find("코노봇") != -1:
                                                    ok.append(channel.id)
                                                    break
                                    for i in ok:
                                        channel = self.bot.get_channel(i)
                                        try:
                                            await channel.send(embed=embed)
                                            success += 1
                                        except discord.Forbidden:
                                            failed += 1
                                            pass
                                    await self.bot.get_channel(884219305942740992).send("코노스바 새글 알림 루프 결과\n성공: {ok}\n실패: {no}\n링크: {url}".format(
                                                                                                ok=success,
                                                                                                no=failed,
                                                                                                url = "https://forum.nexon.com/konosubamobile/board_view?thread="+new_threadid
                                                                                            )
                                                                                        )
            except:
                pass
            await self.update_threadid()
            await asyncio.sleep(60*5)
    def cog_unload(self):
        self.notice.cancel()



def setup(bot):
    bot.add_cog(info(bot))
