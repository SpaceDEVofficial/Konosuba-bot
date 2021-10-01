import io
import random

import discord
from discord.ext import commands

class owner(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="공지")
    @commands.is_owner()
    async def broadcasting(self,ctx,*,value):
        em = discord.Embed(
            title="Konosuba 봇 공지사항!",
            description=value,
            colour=discord.Colour.green()
        )
        em.set_thumbnail(url="https://i.imgur.com/mKq53H3.png")
        em.set_image(url="https://i.imgur.com/ZreNR44.png")
        em.set_footer(text="특정 채널에 받고싶다면 채널주제에 '코노봇'을 입력하세요! 권한 확인 필수!")
        msg = await ctx.reply("발송중...")
        guilds = self.bot.guilds
        ok = []
        ok_guild = []
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
                        ok_guild.append(guild.id)
                        break

        for guild in guilds:
            channels = guild.text_channels
            for channel in channels:
                if guild.id in ok_guild:
                    break
                random_channel = random.choices(channels)
                ok.append(random_channel[0].id)
                break
        for i in ok:
            channel = self.bot.get_channel(i)
            try:
                await channel.send(embed=em)
                success += 1
            except discord.Forbidden:
                failed += 1
                pass
        await msg.edit("발송완료!\n성공: `{ok}`\n실패: `{no}`".format(ok=success,no=failed))



def setup(bot):
    bot.add_cog(owner(bot))
