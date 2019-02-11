import time
import zmq
import base64
import os
import cv2
import threading
import sys

IPcameras = {}
IPcameras["Gallup@NM"] = "http://207.192.232.2:8000/mjpg/video.mjpg?timestamp=1548280479340"
IPcameras["Agua Fria@NM"] = "http://166.241.180.137/mjpg/video.mjpg?timestamp=1548281679736"
IPcameras["Bolton@CT"] = "http://166.248.11.128/mjpg/video.mjpg?timestamp=1548281838022"
IPcameras["El Paso@TX"] = "http://209.194.208.53/mjpg/video.mjpg?timestamp=1548281942187"
IPcameras["Jamestown@ND"]= "http://64.77.205.67/mjpg/video.mjpg"
IPcameras["Newark@NY"] = "http://166.140.227.198/mjpg/video.mjpg?timestamp=1548369639459"
IPcameras["Brighton@MA"] = "http://128.197.128.161/mjpg/video.mjpg"
IPcameras["KL@Malaysia"] = "http://58.26.96.56/mjpg/video.mjpg"
IPcameras["Taegu@Korea"] = "http://220.73.58.90/mjpg/video.mjpg"
IPcameras["Newark2@NY"] = "http://108.53.114.166/mjpg/video.mjpg"
IPcameras["Louisville@KY"] = "http://74.142.179.46:81/mjpg/video.mjpg?timestamp=1548535207899"
IPcameras["Richmond@VA"] = "http://50.73.9.194/mjpg/video.mjpg"
IPcameras["Rancho@CA"] ="http://166.165.58.225/mjpg/video.mjpg?timestamp=1548608344038"
IPcameras["Fayetteville@NC"] = "http://65.40.167.160/mjpg/video.mjpg"
IPcameras["Newyork"] = "http://67.77.134.186:8001/mjpg/video.mjpg"
IPcameras["SanJose@CA"] = "http://50.252.187.219/mjpg/video.mjpg?timestamp=1548704853592"

def producer(source, limit):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect("tcp://10.0.0.9:5556")
#    zmq_socket.setsockopt(zmq.LINGER, -1)
    source_url = IPcameras[source]
    print("Capturing video stream from ", source)
    start = time.time()

    capture = cv2.VideoCapture(source_url)
    i = 0

    while i<limit:
        ret, frame = capture.read()
        if frame is not None:
            i+=1
            ret, buff = cv2.imencode('.jpg', frame)
            message = base64.b64encode(buff)
            meta_data = {'camera' : source.replace("@","_"),
                    'url':source_url,
                    'counter':str(i),
                    'time':str(time.time())}
            zmq_socket.send_json(meta_data, flags=zmq.SNDMORE)
            zmq_socket.send(message)
        else:
            print("Source not available - terminate.")
            break
        time.sleep(.02)
    end = time.time()
    elasped =int((end-start))
    print("%d images captured in %d seconds." % (i, elasped))
    capture.release()

if __name__=="__main__":
#    producer(str(sys.argv[1]), int(sys.argv[2]))

   t1 = threading.Thread(target = producer, args=(sys.argv[1],int(sys.argv[3]),))
   t2 = threading.Thread(target = producer, args=(sys.argv[2],int(sys.argv[3]),))
   t1.start()
   t2.start()
