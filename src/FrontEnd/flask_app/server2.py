from flask import Flask, render_template, send_file, Response, request, flash, stream_with_context
import base64, zmq
import time
import cv2
import numpy as np
import urllib
import time

IP = "tcp://*:5558"
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

def bubble_insert(array, number):
# Insert a new number into the numpy array.
    i = 0
    pop_num = array[-1]
    while number<array[i] and i<len(array):
        i+=1
    array[i+1:] = array[i:-1]
    array[i]=number

    return pop_num

class Dory:
# A very lightweight prototype database in memory. Named after Dolly the goldfish with very short memory.
    def __init__(self, maxsize = 16):
        self.limit = maxsize
        self.record = dict()
# A buffer that saves the data. We want it to maintain a order sorted by the "counter" key
# but don't want to sort the dictionary every time. The maximum number of the dictionary is "maxsize".
        self.bookkeeper =dict()
        self.output = [None]*3

# A dictionary /that keeps track of the order of the buffer dictionary items.

    def look(self, meta_data, message):
        pop_num=0
        try:
            camera_name = meta_data["camera"]
            timestamp = int(meta_data["time"])
            counter = int(meta_data["counter"])
            boxes = meta_data["boxes"]
            if camera_name not in self.record:
                self.record[camera_name] ={counter:[timestamp, boxes, message]}
                self.bookkeeper[camera_name] = np.zeros(self.limit).astype("int")
                self.bookkeeper[camera_name][0]=counter
            else:
                self.record[camera_name][counter] = [timestamp, boxes, message]
                pop_num = bubble_insert(self.bookkeeper[camera_name],counter)
                if pop_num>0:
                    self.output = self.record[camera_name][pop_num]
                    self.record[camera_name].pop(pop_num)
        except Exception as e:
            print("{0} occurred during operation".format(e))
        return pop_num

        def count(self):
# reserved for future improvements.
            pass

dory = Dory()
async def trigger(websocket,path):
    while True:
        meta_data = consumer_receiver.recv_json()
        img_msg = consumer_receiver.recv()
        pop_num=dory.look(meta_data, img_msg)
        if pop_num>0:
            camera_name = meta_data["camera"]
            timestamp, boxes, img_msg = dory.output
    #    timestamp = int(float(meta_data["time"])*1000)
    #    counter = int(meta_data["counter"])
    #    boxes = meta_data["boxes"]
            counter = int(pop_num)
    #        buffer = base64.b64decode(img_msg)
    #        img = cv2.imdecode(np.frombuffer(buffer, np.uint8),cv2.IMREAD_ANYCOLOR)
    #        overlay_boxes(boxes,img)
    #        img_bytes = base64.b64encode(cv2.imencode('.jpg',img)[1].tobytes())
    #        img_bytes=urllib.parse.quote(img_bytes)
            message = {
                "camera": camera_name,
                "img_b64": img_msg,
                "counter": counter,
                "timestamp":timestamp,
                "boxnum": len(boxes)
                }
            await websocket.send(json.dumps(message))
            await asyncio.sleep(0.02)

start_server = websockets.serve(trigger, '0.0.0.0',5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
