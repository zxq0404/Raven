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


IPcameras["mall@LA"] = "http://157.242.44.67/mjpg/1/video.mjpg?timestamp=1548286513419"

stream_dir = "/home/ubuntu/CameraStream/"

Camera_propid = {0:"CV_CAP_PROP_POS_MSEC",
                1:"CV_CAP_PROP_POS_FRAMES",
                2:"CV_CAP_PROP_POS_AVI_RATIO",
                3: "CV_CAP_PROP_FRAME_WIDTH",
                4: "CV_CAP_PROP_FRAME_HEIGHT",
                5: "CV_CAP_PROP_FPS",
                6: "CV_CAP_PROP_FOURCC",
                7: "CV_CAP_PROP_FRAME_COUNT",
                8: "CV_CAP_PROP_FORMAT",
                9: "CV_CAP_PROP_MODE",
                10: "CV_CAP_PROP_BRIGHTNESS",
                11: "CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).",
                12: "CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).",
                13: "CV_CAP_PROP_HUE Hue of the image (only for cameras).",
                14: "CV_CAP_PROP_GAIN Gain of the image (only for cameras).",
                15: "CV_CAP_PROP_EXPOSURE Exposure (only for cameras).",
                16: "CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.",
                17: "CV_CAP_PROP_WHITE_BALANCE_U The U value of the whitebalance setting (note: only supported by DC1394 v 2.x backend currently)",
                18: "CV_CAP_PROP_WHITE_BALANCE_V The V value of the whitebalance setting (note: only supported by DC1394 v 2.x backend currently)",
                19: "CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)",
                20: "CV_CAP_PROP_ISO_SPEED The ISO speed of the camera (note: only supported by DC1394 v 2.x backend currently)",
                21: "CV_CAP_PROP_BUFFERSIZE Amount of frames stored in internal buffer memory (note: only supported by DC1394 v 2.x backend currently)"
                }

def get_res(camera_name):
    url = IPcameras[camera_name]
    capture = cv2.VideoCapture(url)
    if capture.isOpened():
        width = capture.get(3)
        height = capture.get(4)
        frame_rate = capture.get(5)
        print("Camera ", camera_name,":",width, "*", height,",",frame_rate," frame/s")
    else:
        print("Camera ", camera_name, " cannot be accessed.")
    capture.release()

def CVcapture(camera_name, num=100, start = 0, path = "/home/ubuntu/CameraStream/"):
    url = IPcameras[camera_name]
    capture = cv2.VideoCapture(url)
    path = path+camera_name+"/"
    if os.path.exists(path) and os.path.isdir(path):
        pass
    else:
        os.makedirs(path)
    i=start
    while i<num:
    # Capture frame-by-frame
        ret, frame = capture.read()
        i+=1
        if frame is not None:
            resized_frame = cv2.resize(frame,(640,480))
            cv2.imwrite(path+'captured_{index}.png'.format(index=i),resized_frame)
           # cv2.imwrite(path+'captured_{index}.png'.format(index=i),frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
    capture.release()
#cv2.destroyAllWindows()
