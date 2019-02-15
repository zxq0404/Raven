import base64
import io
import zmq
import cv2
import os
import numpy as np
import tensorflow as tf

class CarDetector(object):
    def __init__(self, frozen_graph):

        #Tensorflow localization/detection model
        # Single-shot-dectection with mobile net architecture trained on COCO dataset

        # setup tensorflow graph
        self.detection_graph = tf.Graph()

        # configuration for possible GPU use
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True

        # load frozen tensorflow detection model and initialize
        # the tensorflow graph

        with tf.gfile.GFile(frozen_graph, "rb") as f:
            self.graph_def = tf.GraphDef()
            self.graph_def.ParseFromString(f.read())

        # import the graph_def into a new Graph and returns it
        with self.detection_graph.as_default():
            tf.import_graph_def(self.graph_def, name="")

            self.sess = tf.Session(graph=self.detection_graph, config=config)
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
              # Each box represents a part of the image where a particular object was detected.
            self.boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
              # Each score represent how level of confidence for each of the objects.
              # Score is shown on the result image, together with the class label.
            self.scores =self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_detections =self.detection_graph.get_tensor_by_name('num_detections:0')
        self.image_width = 640
        self.image_height = 480

 #   def box_normal_to_pixel(self, box):
  #      box_pixel = [int(box[0]*self.image_height), int(box[1]*self.image_width), int(box[2]*self.image_height), int(box[3]*self.image_width)]
   #     return np.array(box_pixel)

    def detect(self, image):
        """
        Args:
            image: camera image

        Returns:
            list of bounding boxes: coordinates [y_up, x_left, y_down, x_right]

        """
        self.image_width = image.shape[0]
        self.image_height = image.shape[1]

        with self.detection_graph.as_default():
            image_expanded = np.expand_dims(image, axis=0)
            (boxes, scores, classes, num_detections) = self.sess.run(
                [self.boxes, self.scores, self.classes, self.num_detections],
                feed_dict={self.image_tensor: image_expanded})

            self.out_boxes = np.squeeze(boxes)
            self.out_classes = np.squeeze(classes).astype("int")
            self.out_scores = np.squeeze(scores)
            self.out_number = len(self.out_classes)

    def box_isvalid(self, box, score, category, confidence = 0.3, size_limit = 0.5, ratio_limit = 0.1):
#       Examine whether a detected box is valid (good confidence, reasonable shape and size, etc).
        h = box[2] - box[0]
        w = box[3] - box[1]
        ratio = h/(w+0.01)
        return ratio>ratio_limit and ratio<1/ratio_limit and h<size_limit and w<size_limit and category<9 and score>confidence


    def output(self, confidence =0.3, quiet = True):
        self.car_boxes = []
        category_index={1: {'id': 1, 'name': u'person'},
                        2: {'id': 2, 'name': u'bicycle'},
                        3: {'id': 3, 'name': u'car'},
                        4: {'id': 4, 'name': u'motorcycle'},
                        5: {'id': 5, 'name': u'airplane'},
                        6: {'id': 6, 'name': u'bus'},
                        7: {'id': 7, 'name': u'train'},
                        8: {'id': 8, 'name': u'truck'},
                        9: {'id': 9, 'name': u'boat'},
                        10: {'id': 10, 'name': u'traffic light'},
                        11: {'id': 11, 'name': u'fire hydrant'},
                        13: {'id': 13, 'name': u'stop sign'},
                        14: {'id': 14, 'name': u'parking meter'}}

              # The ID for car in COCO data set is 3
            #idx_vec = [i for i, v in enumerate(cls) if ((v==3) and (scores[i]>0.3))]
        for i in range(self.out_number):
            category = self.out_classes[i]
            score = self.out_scores[i]
            box = self.out_boxes[i]
            if self.box_isvalid(box, score, category):
                box[0] = self.image_width*box[0]
                box[2] = self.image_width*box[2]
                box[1] = self.image_height*box[1]
                box[3] = self.image_height*box[3]
                box = box.astype("int")
                self.car_boxes.append([box[0],box[1],box[2],box[3],score,category])
                if not quiet:
                    print(box, ', confidence: ', self.out_scores[i], ', category: ',category_index[category]['name'])
        if len(self.car_boxes) ==0 and not quiet:
            print('no detection!')

        return self.car_boxes

    def output_as_str(self, confidence =0.3, quiet = True):
        self.output(confidence = confidence, quiet = quiet)
        return [[str(item) for item in box] for box in self.car_boxes]

def DL_init(frozen_graph = "/home/ubuntu/frozen_inference_graph.pb", dummy = cv2.imread("/home/ubuntu/dummy.jpg")):
# Initialize the SSD detector.
    det = CarDetector(frozen_graph)
    det.detect(dummy)
    return det

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

def worker():
# Ingest the data from ZeroMQ queue and apply SSD model. The results will be sent as meta data.
    producer_ip = "tcp://10.0.0.9:5557"
    consumer_ip = "tcp:/10.0.0.6:5558"
    context = zmq.Context()
    detector = DL_init()

    receiver = context.socket(zmq.PULL)
    receiver.connect(producer_ip)
    sender = context.socket(zmq.PUSH)
    sender.connect(consumer_ip)
    print('Ingest images from ', producer_ip)
    print('Send detection results to ', consumer_ip)

    # recieve work

    while True:
        meta_data = receiver.recv_json()
        message = receiver.recv()

        b64_string = base64.b64decode(message)
        img = cv2.imdecode(np.frombuffer(b64_string, np.uint8),cv2.IMREAD_ANYCOLOR)
        detector.detect(img)
        boxes = detector.output_as_str()

        new_meta = {'camera' : meta_data['camera'],
                    'counter':meta_data['counter'],
                    'time': meta_data['time'],
                    'boxes': boxes}

        sender.send_json(new_meta, flags=zmq.SNDMORE)

        overlay_boxes(boxes,img)
        img_bytes = base64.b64encode(cv2.imencode('.jpg',img)[1].tobytes())

        sender.send(img_bytes)
        time.sleep(.01)

if __name__=="__main__":
    worker()
