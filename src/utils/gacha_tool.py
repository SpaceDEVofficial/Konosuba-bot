from .db_tool import DB_tools
from random import choices

gacha_main = {
    "kazuma":[
        "https://media.discordapp.net/attachments/885771035243347978/886429821809344563/1001100.png",
        "https://media.discordapp.net/attachments/885771035243347978/886429812061773834/1003100.png",
        "https://media.discordapp.net/attachments/885771035243347978/886429816717451344/1004116_284830.png"
    ],
    "aqua":[
        "https://media.discordapp.net/attachments/885771035243347978/886430107999277126/1011100.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430113305096192/1013104.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430104979398676/1014107.png"
    ],
    "megumin":[
        "https://media.discordapp.net/attachments/885771035243347978/886430492063305808/1021100_182093.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430494974181426/1023100_182143.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430433695375451/1024118_284860.png"
    ],
    "darkness":[
        "https://media.discordapp.net/attachments/885771035243347978/886430702755803216/1031100_182089.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430705901510687/1033104.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430710779494431/1034100_182073.png"
    ]
}

gacha_icon = {
    "kazuma":[
        "https://media.discordapp.net/attachments/885771035243347978/886429819523436544/1001100_352243.png",
        "https://media.discordapp.net/attachments/885771035243347978/886429810040119336/1003100_352176.png",
        "https://media.discordapp.net/attachments/885771035243347978/886429817271119872/1004116.png"
    ],
    "aqua":[
        "https://media.discordapp.net/attachments/885771035243347978/886430106166362152/1011100_352271.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430110222286878/1013104_352173.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430102462799893/1014107_352200.png"
    ],
    "megumin":[
        "https://media.discordapp.net/attachments/885771035243347978/886430494588284958/1021100_352207.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430495234211890/1023100_352262.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430431262703666/1024118_45321.png"
    ],
    "darkness":[
        "https://media.discordapp.net/attachments/885771035243347978/886430704005697566/1031100_352270.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430705826017291/1033104_352258.png",
        "https://media.discordapp.net/attachments/885771035243347978/886430702374117386/1034100_352260.png"
    ]
}

class gacha:

    def __init__(self,ctx,bot):
        self.bot = bot
        self.ctx = ctx

    def random_gacha(self):
        member = [1, 2, 3]
        weights = [1.5,0.62, 0.162]
        member_choice = choices(["kazuma","aqua","megumin","darkness"])
        member_star = choices(member,weights)
        print(member_star)
        return {"member":str(member_choice[0]),"star":member_star[0]}

    async def GaCha(self):
        coin_check = await DB_tools(ctx=self.ctx,bot=self.bot).get_info()
        if coin_check["type"] == True and coin_check["item"][2] >= 5:
            res = await DB_tools(ctx=self.ctx,bot=self.bot).update_gacha()
            if res:
                member_choice_res = self.random_gacha()
                member_main_img = gacha_main[member_choice_res["member"]][member_choice_res["star"]-1]
                member_icon_img = gacha_icon[member_choice_res["member"]][member_choice_res["star"]-1]
                return {"name":member_choice_res["member"],"main_img":member_main_img,"icon_img":member_icon_img,"star":member_choice_res["star"]}
