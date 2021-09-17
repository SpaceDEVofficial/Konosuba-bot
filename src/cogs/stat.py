import os
import koreanbots
import UniqueBotsKR
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv(verbose=True)

class MyStatcordCog(commands.Cog):
    """
    봇상태를 업데이트하는 그룹이야!
    """
    def __init__(self, bot):
        self.bot = bot
        self.kb = koreanbots.Koreanbots(self.bot, os.getenv("KBTOKEN"), run_task=True)
        self.ub = UniqueBotsKR.client(self.bot, token=os.getenv("UBTOKEN"),autopost=True)

def setup(bot):
    bot.add_cog(MyStatcordCog(bot))
