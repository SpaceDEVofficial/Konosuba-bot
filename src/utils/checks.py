from discord.ext import commands
from .db_tool import DB_tools
from . import execption
import aiosqlite
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

