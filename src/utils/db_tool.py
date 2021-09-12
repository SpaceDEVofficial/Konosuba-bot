import aiosqlite
import discord
class DB_tools:
    def __init__(self,ctx,bot):
        self.ctx = ctx
        self.bot = bot

    async def regist(self):
        DB = self.bot.db_con
        cur = await DB.execute("SELECT * FROM user_db WHERE user_id = ?",(self.ctx.author.id,))
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

    async def unregist(self):
        DB = self.bot.db_con
        cur = await DB.execute("SELECT * FROM user_db WHERE user_id = ?",(self.ctx.author.id,))
        db = await cur.fetchone()
        if db != None:
            await DB.execute("DELETE FROM user_db WHERE  user_id = ?",(self.ctx.author.id,))
            await DB.execute("DELETE FROM guild_member WHERE  user_id = ?", (self.ctx.author.id,))
            await DB.execute("DELETE FROM user_gift WHERE  user_id = ?", (self.ctx.author.id,))
            await DB.commit()
            return True
        return False

    async def get_info(self):
        DB = self.bot.db_con
        cur = await DB.execute("SELECT * FROM user_db WHERE user_id = ?", (self.ctx.author.id,))
        db = await cur.fetchone()
        if db != None:
            return {"type":True,"item":db}
        return {"type":False,"item":None}

    async def update_gacha(self):
        try:
            await self.bot.db_con.execute("UPDATE user_db SET quts = quts - 5 WHERE user_id = ?",(self.ctx.author.id,))
            await self.bot.db_con.commit()
            return True
        except:
            return False

