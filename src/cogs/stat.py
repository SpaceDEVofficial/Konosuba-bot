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
        self.kb = koreanbots.Koreanbots(self.bot, 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg4NTcxMjY4MTQ5ODIxNDQ1MCIsImlhdCI6MTYzMTcxNzIxN30.dhlnG2Pg5CpPltiScaFqBLApqFT5yb3ZDEqCSXrxysmclsXevi3Tc07_3clw3cAgRCFbbzKmqdphrk7dJid6TnW4SFEISb-_CilRn4OmbC-BP_ckeNuoVnw7VjJXuOm0rhTdmM7HQOVpKpQZ8RCR2cv1dpn7_riV04Q4gCSGCvM', run_task=True)
        self.ub = UniqueBotsKR.client(self.bot, token='OHVXeHM1ZHR6Qm1RMERnRWJndGd1by9neklvcENiaEhweDU1NDRwczJ6NzhIQVlwL0FEWXZCQzM3NXNUM1dlN1d4V1ozWExFMUhlTXE4N3VaSFVnWlE9PQ==',autopost=True)

def setup(bot):
    bot.add_cog(MyStatcordCog(bot))
