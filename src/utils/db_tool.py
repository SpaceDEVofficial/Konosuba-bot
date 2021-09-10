import aiosqlite
import discord
class DB_tools:
    def __init__(self,ctx,bot):
        self.ctx = ctx
        self.bot = bot

    async def regist(self):
        DB = self.bot.db_con
        cur = await DB.execute("SELECT * FROM user_db WHERE user_id == ?",(self.ctx.author.id,))
        db = await cur.fetchone()
        if db == None:
            await DB.execute("INSERT INTO user_db VALUES (?,?,?,?,?)",
                                  (
                                      self.ctx.author.id,
                                      100,
                                      50,
                                      0,
                                      1000
                                  )
                                  )
            await DB.commit()
            return True
        return False

