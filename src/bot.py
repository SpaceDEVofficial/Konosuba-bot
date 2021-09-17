import os
from utils.create_embed import embeds
import discord
from discord.ext import commands
from tools.autocogs import AutoCogs
import random
from dotenv import load_dotenv
import aiosqlite
import config
from utils.guild_count_loop import start_loop
load_dotenv(verbose=True)


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        AutoCogs(self)
        self.remove_command("help")
    async def on_ready(self):
        """Called upon the READY event"""
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(name=os.getenv("STATUS"),
                                                                                               type=discord.ActivityType.playing))
        print("Bot is ready.")

    async def is_owner(self, user):
        if user.id in config.OWNER:
            return True

    async def on_guild_join(self,guild):
        if guild.id == 653083797763522580:
            return
        em = embeds(guild=guild).guild_join_thx()
        try:
            await guild.owner.send(embed=em)
        except:
            ch = self.get_channel((random.choice(guild.channels)).id)
            await ch.send(embed=em)

    async def create_db_con(self=None):
        MyBot.db_con = await aiosqlite.connect("./utils/db/db.db")
    """async def on_guild_remove(self,guild):
        await self.tracker.remove_guild_cache(guild)"""




INTENTS = discord.Intents.all()
my_bot = MyBot(command_prefix=os.getenv("PREFIX"), intents=INTENTS)


if __name__ == "__main__":
    my_bot.loop.run_until_complete(MyBot.create_db_con())
    my_bot.run(os.getenv('TOKEN'))