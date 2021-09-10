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
        em.set_image(url="https://i.imgur.com/ZreNR44.png")
        return em

    def regist_ok(self):
        em = discord.Embed(
            title="Register Success!",
            description="""
            가입이 완료되었어요!
            가입 보상으로 `쿼츠50개`와 `1,000에리스`를 드립니다!
            """,
            color=discord.Color.from_rgb(54, 57, 63)
        )
        em.set_thumbnail(url="https://i.imgur.com/mKq53H3.png")
        em.set_image(url="https://i.imgur.com/ZreNR44.png")
        em.set_footer(icon_url="https://i.imgur.com/mKq53H3.png",text="원활한 사용을 위해 인터넷 환경이 좋은 곳에서 사용해주세요.")
        return em

    def unregist_ok(self):
        em = discord.Embed(
            title="Unregister Success!",
            description="""
            탈퇴가 완료되었어요!
            다움에도 만날수있길 기원할게요!
            """,
            color=discord.Color.from_rgb(54, 57, 63)
        )
        em.set_thumbnail(url="https://i.imgur.com/mKq53H3.png")
        em.set_image(url="https://i.imgur.com/ZreNR44.png")
        em.set_footer(icon_url="https://i.imgur.com/mKq53H3.png",text="탈퇴 완료.")
        return em

    def unregist_no(self):
        em = discord.Embed(
            title="Unregister Fails",
            description="""
            탈퇴가 완료되지않았어요..
            가입을 안하신것같은데요?
            """,
            color=discord.Color.from_rgb(54, 57, 63)
        )
        em.set_thumbnail(url="https://i.imgur.com/mKq53H3.png")
        em.set_image(url="https://i.imgur.com/ZreNR44.png")
        em.set_footer(icon_url="https://i.imgur.com/mKq53H3.png",text="탈퇴 실패.")
        return em

    def regist_no(self):
        em = discord.Embed(
            title="Register Fails",
            description="""
            이미 가입이 되어있어요... ☹
            """,
            color=discord.Color.from_rgb(54, 57, 63)
        )
        em.set_thumbnail(url="https://i.imgur.com/mKq53H3.png")
        em.set_image(url="https://i.imgur.com/ZreNR44.png")
        return em

    def aqua_skill(self):
        em = discord.Embed()
        em.set_image(url="https://media.discordapp.net/attachments/885771035243347978/885771165463896064/aqua.gif")
        return em

    def idle_embed(self):
        em = discord.Embed(
            title="idle",
            description="idle"
        )
        em.set_thumbnail(url="https://i.imgur.com/mKq53H3.png")
        em.set_image(url="https://i.imgur.com/ZreNR44.png")
        return em