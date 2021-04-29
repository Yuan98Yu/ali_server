# WS client example
import asyncio
import websockets
import json
import time

from config import rec_img_ip, rec_img_port
ws_web_server_url = f'ws://8.131.72.239:{rec_img_port}'
# ws_web_server_url = f'ws://localhost:{rec_img_port}'

data = dict()
data['pred'] = 'cloudy'
data['forecast'] = {
    "obsTime": "2021-04-23T11:32+08:00",
    "temp": "20",
    "feelsLike": "17",
    "icon": "101",
    "wind360": "90",
    "windDir": "\u4e1c\u98ce",
    "windScale": "3",
    "windSpeed": "18",
    "humidity": "48",
    "precip": "0.0",
    "pressure": "1015",
    "vis": "30",
    "cloud": "91",
    "dew": "8",
    "type": "\u591a\u4e91"
}
data = json.dumps(data)


async def hello():
    async with websockets.connect(ws_web_server_url) as websocket:
        global data

        await websocket.send(data)
        print(f"> {data}")


if __name__ == '__main__':
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(hello())
        except Exception as e:
            print(e)

        time.sleep(5)
