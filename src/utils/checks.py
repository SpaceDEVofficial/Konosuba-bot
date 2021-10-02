from discord.ext import commands
from .db_tool import DB_tools
from . import execption
import aiosqlite
from discord.ext import commands
from data import masters

async def require_register(ctx):
    async with aiosqlite.connect("./utils/db/db.db") as db:
        cur = await db.execute("SELECT * FROM user_db WHERE user_id = ?", (ctx.author.id,))
        dbs = await cur.fetchone()
        print(dbs)
        if dbs is None:
            raise execption.PermError.NotRegister
        return True

def require():
    return commands.check(require_register)



async def master_only(ctx):
    if ctx.author.id in masters.MASTERS:
        return True
    raise commands.NotOwner()

def is_master():
    return commands.check(master_only)

async def not_bot(ctx):
    if not ctx.author.bot:
        return True
    raise commands.CheckFailure