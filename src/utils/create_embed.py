import discord

class embeds:
    def __init__(self,ctx=None,bot=None,guild=None):
        self.ctx = ctx
        self.bot = bot
        self.guild = guild


    def guild_join_thx(self):
        em = discord.Embed(
            title="Thank you for invite me!",
            description="""
            저를 초대해주셔서 감사드려요!
            아직 부족한 점이 많겠지만 앞으로 좋은 서비스를 할 수 있도록 노력할게요!
            """,
            color=discord.Color.from_rgb(54,57,63)
           )
        em.set_thumbnail(url="https://i.imgur.com/mKq53H3.png")
        em.set_image(url="../asset/img/logo_kr.png")
        return em