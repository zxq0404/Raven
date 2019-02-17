import time
import zmq
import base64
import os
import cv2
import threading
import sys

# A program that test the available IP cameras.
# Ip camera addresses

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
IPcameras["SanJose@CA"] = "http://50.252.187.219/mjpg/video.mjpg?timestamp=1548619818017"

def get_res(camera_name):
# check whether an IP camera can be connected, and how fast the video capture can be.
    url = IPcameras[camera_name]
    capture = cv2.VideoCapture(url)
    if capture.isOpened():
        width = capture.get(3)
        height = capture.get(4)
        frame_rate = capture.get(5)
        print("Camera ", camera_name,":",width, "*", height,",",frame_rate," frame/s")
        start = time.time()
        for i in range(10):
            ret, frame = capture.read()
        end = time.time()
        print("10 frames takes %f seconds" % (end-start))
    else:
        print("Camera ", camera_name, " cannot be accessed.")
    capture.release()

def main():
    for camera in IPcameras.keys():
        get_res(camera)

if __name__=="__main__":
    main()
