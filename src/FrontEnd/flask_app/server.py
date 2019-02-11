from flask import Flask, render_template, send_file, Response, request, flash, stream_with_context
import base64, zmq
import time
import cv2
import numpy as np
import urllib
import time

IP = "tcp://34.239.152.41:5558"
#        print('consumer started...Ingest images from ', IP)
context = zmq.Context()
    # recieve work
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.connect(IP)

from itertools import cycle
import asyncio
import base64
import datetime
import json
import random
import websockets

start = time.time()

def overlay_boxes(boxes,image):
# Overlay the detected box on the image. It directly modifies the raw images
# so it should only be used for showing the graph.
    for box in boxes:
        x1, y1, x2, y2 = box[:4]
        x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
        image[x1:x1+4,y1:y2+1,:] =0
        image[x2:x2+4,y1:y2+1,:] =0
        image[x1:x2+1,y1:y1+4,:] =0
        image[x1:x2+1,y2:y2+4,:] = 0
        image[x1:x1+3,y1:y2+1,0] = 255
        image[x2:x2+3,y1:y2+1,0] = 255
        image[x1:x2+1,y1:y1+3,0] = 255
        image[x1:x2+1,y2:y2+3,0] = 255



async def trigger(websocket,path):
    while True:
        meta_data = consumer_receiver.recv_json()
        img_msg = consumer_receiver.recv()
        camera_name = meta_data["camera"]
        timestamp = int(float(meta_data["time"])*1000)
        counter = int(meta_data["counter"])
        boxes = meta_data["boxes"]

        buffer = base64.b64decode(img_msg)
        img = cv2.imdecode(np.frombuffer(buffer, np.uint8),cv2.IMREAD_ANYCOLOR)
        overlay_boxes(boxes,img)
        img_bytes = base64.b64encode(cv2.imencode('.jpg',img)[1].tobytes())
        img_bytes=urllib.parse.quote(img_bytes)
        message = {
            "camera": camera_name,
            "img_b64": img_bytes,
            "counter": counter,
            "timestamp":timestamp,
            "boxnum": len(boxes)
        }
        await websocket.send(json.dumps(message))
        await asyncio.sleep(0.02)

start_server = websockets.serve(trigger, '127.0.0.1',5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
