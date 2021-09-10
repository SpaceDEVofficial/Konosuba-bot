import os

from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp

class gencard:

    def __init__(self,bot,ctx):
        self.ctx = ctx
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)


    async def get_avatar(self, user):
        avatar_url = user.avatar_url_as(format="png")
        print(avatar_url)
        async with self.session.get(str(avatar_url)) as response:
            # this gives us our response object, and now we can read the bytes from it.
            avatar_bytes = await response.content.read()
            await self.session.close()
            return avatar_bytes

    async def GenerateInfoCard(self):
        bg = Image.open('./asset/img/infocard.png')
        avatar = await self.get_avatar(user=self.ctx.author)
        print(os.getcwd())
        with open('./utils/profile.jpg', 'wb') as handler:
            handler.write(avatar)
        avt = Image.open('./utils/profile.jpg')
        size = 160
        avt = avt.resize((size, size), resample=0)
        mask_im = Image.new("L", avt.size, 0)
        bgtext = ImageDraw.Draw(bg)
        font = ImageFont.truetype("./utils/user.TTF", 50)

        bgtext.text((60,78), f"{self.ctx.author}", (54,27,10), font=font)
        font = ImageFont.truetype("./utils/user.TTF", 42)
        bgtext.text((60, 207), f"{self.ctx.author.id}", (54, 27, 10), font=font)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((0, 0, size, size), fill=255)
        mask_im.save('./utils/mask_circle.png', quality=100)
        back_im = bg.copy()
        back_im.paste(avt, (600, 79), mask_im)

        back_im.save('./utils/card.png', quality=100)
        return True
