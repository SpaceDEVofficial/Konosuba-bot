import os

import discord
from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp
from .db_tool import DB_tools
class gencard:

    def __init__(self,bot,ctx):
        self.ctx = ctx
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)


    async def get_avatar(self, user:discord.Member):
        avatar_url = user.avatar
        print(avatar_url)
        async with self.session.get(str(avatar_url)) as response:
            # this gives us our response object, and now we can read the bytes from it.
            avatar_bytes = io.BytesIO(await response.read())
            await self.session.close()
            return avatar_bytes

    async def GenerateInfoCard(self):
        datas = await DB_tools(ctx=self.ctx,bot=self.bot).get_info()
        bg = Image.open('./asset/img/infocard.png')
        avatar = await self.get_avatar(user=self.ctx.author)
        print(os.getcwd())
        avt = Image.open(avatar)
        size = 160
        avt = avt.resize((size, size), Image.ANTIALIAS)
        mask_im = Image.new("L", avt.size, 0)
        bgtext = ImageDraw.Draw(bg)
        font = ImageFont.truetype("./utils/user.TTF", 50)

        bgtext.text((60,78), f"{self.ctx.author}", (54,27,10), font=font)
        font = ImageFont.truetype("./utils/user.TTF", 42)
        bgtext.text((60, 207), f"{self.ctx.author.id}", (54, 27, 10), font=font)
        font = ImageFont.truetype("./utils/user.TTF", 20)
        bgtext.text((658, 312), f"{datas['item'][3]}", (54, 27, 10), font=font) #medal
        bgtext.text((658, 356), f"{datas['item'][1]}", (54, 27, 10), font=font)  #stamina
        bgtext.text((658, 400), f"{datas['item'][2]}", (54, 27, 10), font=font)  # quts
        bgtext.text((658, 440), f"{datas['item'][4]}", (54, 27, 10), font=font)  # money
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((0, 0, size, size), fill=255)
        #mask_im.save('./utils/mask_circle.png', quality=100)
        back_im = bg.copy()
        back_im.paste(avt, (600, 79), mask_im)
        bytes = io.BytesIO()
        back_im.save(bytes, 'PNG')
        bytes.seek(0)
        return {"type":True,"img":bytes}
