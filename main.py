# WS server example
import asyncio
import json
import glob
from pathlib import Path
from io import BytesIO
import threading

from PIL import Image
import websockets

from config import (img_save_dir, rec_img_ip, rec_img_port, rec_reqimg_ip,
                    rec_reqimg_port)


async def rec_reqimg(websocket, path):
    await websocket.recv()
    print('rec_reqimg'.center(100, '*'))
    img_idx = len(glob.glob(str(Path(img_save_dir) / Path('*.jpg')))) - 1
    img = Image.open(img_save_dir / Path(f'img_{img_idx}.jpg')).convert('RGB')
    # greeting = f"Hello {name}!"

    await websocket.send(img.tobytes())
    # print(f"> {greeting}")


async def rec_img(websocket, path):
    data = await websocket.recv()
    # data = base64.b64decode(data)
    print('rec data!'.center(100, '='))
    stream = BytesIO(data)
    # img = Image.frombytes('RGB', (320, 320), data)
    img = Image.open(stream).convert('RGB')
    img_idx = len(glob.glob(str(img_save_dir / Path('*.jpg'))))
    img.save(img_save_dir / Path(f'img_{img_idx}.jpg'))


def thread_loop_task(loop, task, server_ip, server_port):
    # 为子线程设置自己的事件循环
    asyncio.set_event_loop(loop)
    # future = asyncio.gather(task)
    start_server = websockets.serve(task, server_ip, server_port)
    loop.run_until_complete(start_server)
    loop.run_forever()


def main():
    # start_server = websockets.serve(rec_img, rec_img_ip, rec_img_port)
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()
    for task_func, server_ip, server_port in [
        (rec_img, rec_img_ip, rec_img_port),
        (rec_reqimg, rec_reqimg_ip, rec_reqimg_port)
    ]:
        thread_loop = asyncio.new_event_loop()

        # 将thread_loop作为参数传递给子线程
        t = threading.Thread(target=thread_loop_task,
                             args=(thread_loop, task_func, server_ip,
                                   server_port))
        t.daemon = True
        t.start()
    while True:
        pass


if __name__ == '__main__':
    main()
