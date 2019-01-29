#!/usr/bin/python

import ts3
from flask import Flask
from flask import send_file
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from datetime import datetime

app = Flask(__name__)

BANNER = "banniere.jpg"
FONT = "font.ttf"
# This text is just used to be drawn on the banner
# the bot will connect to teamspeak on localhost
TS_ADRESSS = "<your_adress_here>"

IMG_OUT = "out.jpg"

TS_LOGIN_NAME = "<login>"
TS_LOGIN_PASSWORD = "<password>"

@app.route("/")
def hello():
        img = Image.open(BANNER)
        connected = str(connected_clients())

        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype(FONT, 200)
        draw.text((50, 10), TS_ADRESSS, (255, 255, 255), font=font)
        top = 500
        left = 50
        draw.text((left, top),connected,(255,255,255),font=font)
        img.save(IMG_OUT)
        # No cache timeout to have connected clients in real time
        return send_file(IMG_OUT, mimetype='Image/jpg', cache_timeout=0, last_modified=datetime.now())

def connected_clients():
        with ts3.query.TS3Connection("localhost") as ts3conn:
                # Note, that the client will wait for the response and raise a
                # **TS3QueryError** if the error id of the response is not 0.
                try:
                        ts3conn.login(
                                client_login_name=TS_LOGIN_NAME,
                                client_login_password=TS_LOGIN_PASSWORD
                        )
                except ts3.query.TS3QueryError as err:
                        return 0

                ts3conn.use(sid=1)

                # Each query method will return a **TS3QueryResponse** instance,
                # with the response.
                resp = ts3conn.clientlist()
                return len(resp.parsed) - 1


if __name__ == '__main__':
    app.run()
