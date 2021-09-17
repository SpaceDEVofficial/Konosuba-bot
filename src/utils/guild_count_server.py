from datetime import datetime
import matplotlib.pyplot as plt
import flask
import quart
from quart import request
from io import BytesIO
import aiosqlite

async def out():
    async with aiosqlite.connect("db/db.db") as con:
        data = await (await con.execute("SELECT * FROM guild_count")).fetchall()
        x = []
        y = []
        for i in data:
            x.append(i[0])
            y.append(i[1])
        #x = [datetime.strptime(date, "%Y/%m/%d %H:%M").date() for date in datas]
        print(y,x)
        fig, ax = plt.subplots()
        ax.set(title='Konosuba bot Server chart!')
        plt.plot_date(x, y, linestyle='solid')
        plt.gcf().set_size_inches(8, 6)
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