import discord
from discord.ext import commands
from discord.errors import Forbidden

"""This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command('help')" in your bot, and the command must be in a cog for it to work.

Original concept by Jared Newsom (AKA Jared M.F.)
[Deleted] https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b
Rewritten and optimized by github.com/nonchris
https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2

You need to set three variables to make that cog run.
Have a look at line 51 to 57
"""


async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("임베드를 보낼 수 없어.. 권한 확인해줘! :)")
        except Forbidden:
            await ctx.author.send(
                f"{ctx.channel.name}이라느 채널명을 가진 {ctx.guild.name}에 임베드를 보낼수없어..\n"
                f"나 대신 알려줄래? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """
    Sends this help message
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="도움",aliases= [ '도움말', '명령어', 'commands' ])
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def helps(self, ctx, *input):
        """Shows all modules of that bot"""
	
        # !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
        global emb
        prefix ='kn!'
        version ='1.0beta'
        
        # setting owner name - if you don't wanna be mentioned remove line 49-60 and adjust help text (line 88) 
        owner = '281566165699002379'# ENTER YOU DISCORD-ID
        owner_name = 'gawi#9537'# ENTER YOUR USERNAME#1234

            # checks if cog parameter was given
            # if not: sending all modules and commands not associated with a cog
        if not input:
            # checks if owner is on this server - used to 'tag' owner
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner

            # starting to build embed
            emb = discord.Embed(title='도움말', color=discord.Color.blue(),
                                description=f'Use `{prefix}도움 <그룹명>` 으로 더 자세한 도움말을 확인할수있어! '
                                            f':smiley:\n')

            # iterating trough cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            # adding 'list' of cogs to embed
            emb.add_field(name='그룹', value=cogs_desc, inline=False)

            # integrating trough uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # adding those commands to embed
            if commands_desc:
                emb.add_field(name='그룹에 속하지 않음', value=commands_desc, inline=False)

            # setting information about author
            emb.add_field(name="About", value=f"이 명령어는 `Chriѕ#0001`님이 만드신소스를 활용하였습니다.\n\
                                    [링크](<https://github.com/nonchris/discord-fury>)")
            emb.set_footer(text=f"버전: {version}")

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # found cog - breaking loop
                    break

            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                emb = discord.Embed(title="뭐지..?",
                                    description=f"너가 입력한 `{input[0]}` (은)는 들은적이 없는건데..? :scream:",
                                    color=discord.Color.orange())

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(title="너무 많아..",
                                description="하나의 그룹명만 입력해주라.. :sweat_smile:",
                                color=discord.Color.orange())
            # sending reply embed using our own function defined above
        await send_embed(ctx, emb)


def setup(bot):
    bot.add_cog(Help(bot))
