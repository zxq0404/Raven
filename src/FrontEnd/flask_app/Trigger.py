import base64, zmq
import time
import cv2
import numpy as np
import urllib
import time

IP = "tcp://*:5560"
context = zmq.Context()
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.bind(IP)
# Initialize message receiving

from itertools import cycle
import asyncio
import base64
import datetime
import json
import random
import websockets

start = time.time()


async def trigger(websocket,path):
# Receive ZeroMQ message and send it to the webpage.
    while True:
        meta_data = consumer_receiver.recv_json()
        img_msg = consumer_receiver.recv()

        camera_name = meta_data["camera"]
        timestamp = int(meta_data["time"])
        counter = int(meta_data["counter"])
        boxes = meta_data["boxes"]

        buffer = base64.b64decode(img_msg)
# Has to use urllib to deal with exotic characters.
        img_bytes=urllib.parse.quote(img_msg)
        message = {
            "camera": camera_name,
            "img_b64": img_bytes,
            "counter": counter,
            "timestamp":timestamp,
            "boxnum": len(boxes)
        }
        await websocket.send(json.dumps(message))
        await asyncio.sleep(0.001)

# Note: websockets only works with 0.0.0.0
start_server = websockets.serve(trigger, '0.0.0.0',5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
