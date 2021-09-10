from PIL import Image, ImageDraw
import io
import aiohttp

class gencard:

    def __init__(self,bot,ctx):
        self.ctx = ctx
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)


    async def get_avatar(self, user):
        avatar_url = user.avatar_url_as(format="png")

        async with self.session.get(avatar_url) as response:
            # this gives us our response object, and now we can read the bytes from it.
            avatar_bytes = await response.read()

        return avatar_bytes


    async def GenerateInfoCard(self,ctx):
        async with Image.open(io.BytesIO('./asset/img/infocard.png')) as bg:
            avatar = await self.get_avatar(user=ctx.author)
            async with Image.open(io.BytesIO(avatar)) as avt:
                bg.paste(avt,(5,5))
                return bg.save(io.BytesIO,'png')
