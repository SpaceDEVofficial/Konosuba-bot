import discord
from discord.ext import commands
from utils.create_embed import embeds
from utils.db_tool import DB_tools
from utils.gacha_tool import gacha
import asyncio
"""class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.value = False
        self.stop()"""
class game(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="스킬")
    async def skill(self,ctx):
        em = embeds().aqua_skill()
        msg = await ctx.reply(embed=em)
        await asyncio.sleep(2.9)
        em = embeds().idle_embed()
        await msg.edit(embed=em)

    @commands.command(name="뽑기")
    async def gacha(self,ctx):
        res = await gacha(ctx=ctx,bot=self.bot).GaCha()
        msg = await embeds(ctx=ctx).gacha_loading_embed()
        await asyncio.sleep(5.0)
        await msg.delete()
        await ctx.reply(embed=embeds().gacha_res_embed(name=res["name"], star=res["star"], main_img=res["main_img"],
                                                        icon_img=res["icon_img"]))


def setup(bot):
    bot.add_cog(game(bot))
