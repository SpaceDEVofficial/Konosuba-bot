import discord
from discord.ext import commands
import asyncio
from data import colors
from utils.basecog import BaseCog
from utils import rchatmgr
from datetime import timedelta
import time
import math
from typing import Optional
from itertools import cycle
import random
from db import randnick
from pycord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)
class MainCmds(BaseCog):
    """
    랜덤채팅을 처리하는 그룹이야!
    """
    def __init__(self, bot):
        super().__init__(bot)

    @commands.dm_only()
    @commands.command(name='랜덤채팅',help="**`kn!랜덤채팅 [인원]`**\n> DM에서, 입력한 인원으로 랜덤채팅 매칭을 시작합니다. 인원수는 자신을 포함하며 입력하지 않으면 2인으로 시작됩니다.")
    async def _randchat(self, ctx: commands.Context, count: Optional[int]=2):
        if not 2 <= count:
            await ctx.send(
                embed=discord.Embed(
                    title="❗ 인원수는 최소 2명입니다!",
                    description="인원수는 자신도 포함한 수입니다!",
                    color=colors.ERROR
                )
            )

        msg = await ctx.send(
            embed=discord.Embed(
                title=f'💬 {count}인 개인 랜덤채팅 매칭을 시작할까요?',
                description=f'자신을 포함해 전체 {count}명을 매칭하게 됩니다.\n\n**채팅 모드를 선택하세요:**\n\n🏷: **일반 모드**\n> 이름과 태그가 표시됩니다.\n\n❔: **익명 모드**\n> 이름과 태그 대신 랜덤으로 생성한 닉네임을 사용합니다.',
                color=colors.PRIMARY
            ).set_footer(text="❌ 를 클릭해 취소합니다."),
            components=[
                [Button(custom_id="normal", style=1,emoji="🏷"),
                Button(custom_id="nick", style=1,emoji="❔"),
                 Button(custom_id="no", style=4,emoji="❌")]
            ]

        )

        checkemj = '✅'
        crossemj = '❌'
        emjs = '🏷', '❔', crossemj
        """
        for emj in emjs:
            await msg.add_reaction(emj)
        """

        try:
            interaction = await self.bot.wait_for("button_click",
                                                  check=lambda i: i.user.id == ctx.author.id and i.message.id == msg.id,
                                                  timeout=30)
            name = interaction.custom_id
            print(name)
        except asyncio.TimeoutError:
            await msg.delete()
            return
        await msg.delete()
        if name != "no":
            if self.rmgr.is_in_queue(ctx.author.id):
                return

            if name == "nick":
                altnick = ' '.join([random.choice(randnick.FIRST), random.choice(randnick.LAST)])
            else:
                altnick = None

            rainbow = cycle(map(lambda x: x/35, range(0, 36)))

            def get_matching_embed(time_elapsed_seconds: float=None):
                embed = discord.Embed(
                    title='{} 채팅 상대를 매칭 중입니다...'.format(self.emj.get(ctx, "loading")),
                    color=discord.Color.from_hsv(next(rainbow), 1, 0.9)
                )

                footermsg = '❌ 로 반응해 매칭을 취소할 수 있습니다.'

                if time_elapsed_seconds:
                    embed.set_footer(text=f"{footermsg} {timedelta(seconds=time_elapsed_seconds)} 지남")
                else:
                    embed.set_footer(text=footermsg)

                return embed

            start = time.time()

            matchmsg = await ctx.send(
                embed=get_matching_embed(0),
                components=[
                     Button(custom_id="no", style=4, emoji="❌")
                ]
            )

            async def cancel_waitfor():
                try:
                    interaction = await self.bot.wait_for("button_click", check=lambda
                        i: i.user.id == ctx.author.id and i.message.id == matchmsg.id )
                    name = interaction.custom_id
                    if name == "no":
                        self.rmgr.cancel_match(ctx.author.id)
                finally:
                    self.rmgr.cancel_match(ctx.author.id)

            async def time_elapsed_counter():
                while True:
                    await matchmsg.edit(
                        embed=get_matching_embed(math.trunc(time.time() - start)),
                        components=[
                             Button(custom_id="no", style=4, emoji="❌")
                        ]

                    )
                    await asyncio.sleep(1)

            cancel_task = asyncio.create_task(cancel_waitfor())
            time_counter_task = asyncio.create_task(time_elapsed_counter())

            try:
                match = await self.rmgr.start_match(ctx.author.id, count=count-1, altnick=altnick, timeout=5*60)
            except asyncio.TimeoutError:
                cancel_task.cancel()
                time_counter_task.cancel()
                try:
                    await matchmsg.delete()
                finally:
                    await ctx.send(
                        embed=discord.Embed(
                            title='⏰ 매칭 상대를 찾지 못했습니다. 시간이 초과되었습니다!',
                            color=colors.ERROR
                        )
                    )

            except rchatmgr.MatchCanceled:
                cancel_task.cancel()
                time_counter_task.cancel()
                try:
                    await matchmsg.delete()
                finally:
                    await ctx.send(
                        embed=discord.Embed(
                            title='❌ 매칭을 취소했습니다.',
                            color=colors.ERROR
                        )
                    )

            else:
                cancel_task.cancel()
                time_counter_task.cancel()
                try:
                    await matchmsg.delete()
                finally:
                    members = "`" + "`님, `".join(o.altnick or str(self.bot.get_user(o.uid)) for o in match if o.uid != ctx.author.id) + "`"
                    await ctx.send(
                        embed=discord.Embed(
                            title=f'{checkemj} 매칭됐습니다!',
                            description=(f'당신의 별명은 `{altnick}` 입니다!\n' if altnick else '') + members + '와(과) 매칭되었습니다.',
                            color=colors.SUCCESS
                        ).set_footer(text=f'{self.bot.command_prefix}나가기 명령으로 랜덤채팅에서 나갈 수 있습니다.')
                    )

            finally:
                cancel_task.cancel()
                time_counter_task.cancel()

    @commands.dm_only()
    @commands.command(name="나가기",help="**`kn!나가기`**\n> 랜덤채팅을 나갑니다. 남은 사람들은 계속 채팅이 진행됩니다.")
    async def _exit(self, ctx: commands.Context):
        if self.rmgr.is_matched(ctx.author.id):
            msg = await ctx.author.send(
                "정말로 진행중인 랜덤채팅에서 나갈까요?",
                components=[
                    [Button(label="Confirm", custom_id="yes", style=1),
                    Button(label="Cancel", custom_id="no", style=4)]
                ]
            )
            try:
                interaction = await self.bot.wait_for("button_click", check=lambda
                    i: i.user.id == ctx.author.id and i.message.id == msg.id, timeout=30)
                name = interaction.custom_id
            except asyncio.TimeoutError:
                await msg.delete()
                return
            if name == "yes":
                await msg.edit("나가기를 선택하셨습니다.",components=[])
                match = self.rmgr.get_matched(ctx.author.id)
                mymatch = next((m for m in match if m.uid == ctx.author.id), None)
                #match.remove(mymatch)
                nick = mymatch.altnick or ctx.author
                self.rmgr.exit_match(ctx.author.id)
                await ctx.author.send(
                    embed=discord.Embed(
                        title="↩ 랜덤 채팅을 나갔습니다!",
                        color=colors.SUCCESS
                    )
                )

                await asyncio.gather(
                    *(
                        one.send(
                            embed=discord.Embed(
                                description=f"**`{nick}` 님이 채팅을 나갔습니다!**",
                                color=colors.WARN
                            )
                        )
                        for one in map(self.bot.get_user, map(lambda x: x.uid, match)) if one.id != ctx.author.id
                    ),
                    return_exceptions=True
                )

                if len(match) == 2:
                    await self.bot.get_user(list(filter(lambda x: x.uid != ctx.author.id, match))[0].uid).send(
                        embed=discord.Embed(
                            description="대화 상대가 모두 나가 랜덤채팅이 종료되었습니다.",
                            color=colors.PRIMARY
                        )
                    )
            else:
                await msg.delete()
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="❌ 이 명령어는 랜덤채팅 중에만 사용할 수 있습니다!",
                    description="이미 채팅을 나간것으로 보입니다!",
                    color=colors.ERROR
                )
            )

    @commands.dm_only()
    @commands.command(name="참여자",help="**`kn!참여자`**\n> 현재 랜덤채팅에 참여한 사람의 목록을 확인합니다.")
    async def _people(self, ctx: commands.Context):
        if self.rmgr.is_matched(ctx.author.id):
            match = self.rmgr.get_matched(ctx.author.id)
            
            await ctx.send(
                embed=discord.Embed(
                    title="📋 채팅 참여자 목록",
                    description="\n".join(map(lambda x: (x.altnick or str(self.bot.get_user(x.uid))) + (' (나)' if x.uid == ctx.author.id else ''), match)),
                    color=colors.PRIMARY
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="❌ 이 명령어는 랜덤채팅 중에만 사용할 수 있습니다!",
                    color=colors.ERROR
                )
            )


def setup(bot):
    cog = MainCmds(bot)
    bot.add_cog(cog)
