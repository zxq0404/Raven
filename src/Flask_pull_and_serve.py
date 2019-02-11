from flask import Flask, render_template, send_file, Response
import base64, zmq
import time
import cv2
import numpy as np

dummy = open("/Users/Xiaoqing/Insight/CV2capture/Received/SanJose_CA_1.jpg","rb").read()

IP = "tcp://18.232.52.148:5557"
#        print('consumer started...Ingest images from ', IP)
context = zmq.Context()
    # recieve work
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.connect(IP)

def work():
    buffer = dummy
    while True:
        meta_data = consumer_receiver.recv_json()
        message = consumer_receiver.recv()
        buffer = base64.b64decode(message)
        boxes = meta_data['boxes']
        img = cv2.imdecode(np.frombuffer(buffer, np.uint8),cv2.IMREAD_ANYCOLOR)
        overlay_boxes(boxes,img)
        img_bytes = cv2.imencode('.jpg',img)[1].tobytes()
        yield gen(img_bytes)

def gen(buffer):
    return (b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + buffer + b'\r\n')

def overlay_boxes(boxes,image):
# Overlay the detected box on the image. It directly modifies the raw images
# so it should only be used for showing the graph.
    for box in boxes:
        x1, y1, x2, y2 = box[:4]
        x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
        image[x1:x1+5,y1:y2+1,:] =0
        image[x2:x2+5,y1:y2+1,:] =0
        image[x1:x2+1,y1:y1+5,:] =0
        image[x1:x2+1,y2:y2+5,:] = 0
        image[x1:x1+5,y1:y2+1,0] = 255
        image[x2:x2+5,y1:y2+1,0] = 255
        image[x1:x2+1,y1:y1+5,0] = 255
        image[x1:x2+1,y2:y2+5,0] = 255

app = Flask(__name__)
@app.route('/')
@app.route('/index')
def video_feed():
    return Response(work(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(host="0.0.0.0")
