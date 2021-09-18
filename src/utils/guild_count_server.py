from datetime import datetime
import matplotlib.pyplot as plt
import flask
import quart
from quart import request
from io import BytesIO
import aiosqlite
import math
import warnings

warnings.filterwarnings("ignore")
async def out():
    async with aiosqlite.connect("db/db.db") as con:
        data = list(await (await con.execute("SELECT * FROM guild_count")).fetchall())
        if len(data) > 50:
            data = data[(len(data)-50):]
        x = []
        y = []
        for i in data:
            x.append(i[1][:-3])
            y.append(i[0])
        #x = [datetime.strptime(date, "%Y/%m/%d %H:%M").date() for date in datas]
        print(y,x)
        fig, ax = plt.subplots()
        ax.set(title='Konosuba bot Server chart!')
        plt.plot_date(x, y, linestyle='solid')
        plt.gcf().set_size_inches(20, 10)
        new_list = range(math.floor(min(y)), math.ceil(max(y)) + 1)
        plt.yticks(new_list)
        ax.xaxis.set_tick_params(rotation=35, labelsize=10)
        bytesio = BytesIO()
        plt.savefig(bytesio, dpi=300, format='png')
        bytesio.seek(0)
        return bytesio

app = quart.Quart(__name__)


@app.route("/get")
async def web_get_image():
    if request.args.get('type') == 'image':
        return await quart.send_file(filename_or_io=await out(), mimetype='image/png')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)