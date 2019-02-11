from itertools import cycle
import asyncio
import datetime
import json
import websockets

from flask import Flask, render_template, send_file, Response, request, flash, stream_with_context
import base64, zmq
import time
import cv2
import numpy as np
import urllib

start = time.time()
IP="tcp://35.175.180.11:5558"
#        print('consumer started...Ingest images from ', IP)
context = zmq.Context()
    # recieve work
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.connect(IP)

async def trigger(websocket, path):
    while True:
        meta_data = consumer_receiver.recv_json()
        img_msg = consumer_receiver.recv()
        camera_name = meta_data["camera"]
        timestamp = float(meta_data["time"])-start
        counter = int(meta_data["counter"])
        boxes = meta_data["boxes"]

        buffer = base64.b64decode(img_msg)
        img = cv2.imdecode(np.frombuffer(buffer, np.uint8),cv2.IMREAD_ANYCOLOR)
        overlay_boxes(boxes,img)
        img_bytes = base64.b64encode(cv2.imencode('.jpg',img)[1].tobytes())
        img_bytes=urllib.parse.quote(img_bytes)
        message = {
            "img_b64": img_bytes,
            "counter": counter,
            "timestamp":timestamp,
            "boxnum": len(boxes)
        }
        await websocket.send(json.dumps(message))
        await asyncio.sleep(0.05)

start_server = websockets.serve(trigger, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
