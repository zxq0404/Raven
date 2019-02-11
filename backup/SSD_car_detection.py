import contextlib
import time

import cv2
import os
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
import matplotlib.patches as patches
%matplotlib inline

class CarDetector(object):
    def __init__(self, frozen_graph):

        self.car_boxes = []
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

    def box_normal_to_pixel(self, box):
        box_pixel = [int(box[0]*self.image_height), int(box[1]*self.image_width), int(box[2]*self.image_height), int(box[3]*self.image_width)]
        return np.array(box_pixel)

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

            self.out_boxes=np.squeeze(boxes)
            self.out_classes =np.squeeze(classes)
            self.out_scores = np.squeeze(scores)

        return self.out_boxes, self.out_classes, self.out_scores

    def output(self, confidence =0.3, quiet = False):
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
        idx_vec = [i for i, v in enumerate(self.out_classes) if ((v<9) and (self.out_scores[i]>confidence))]

        if len(idx_vec) ==0 and not quiet:
            print('no detection!')
        else:
            for idx in idx_vec:
                box = self.box_normal_to_pixel(self.out_boxes[idx])
                box_h = box[2] - box[0]
                box_w = box[3] - box[1]
                ratio = box_h/(box_w + 0.01)
                v = self.out_classes[idx]

          #          if ((ratio < 0.8) and (box_h>20) and (box_w>20)):
           #             tmp_car_boxes.append(box)
                if not quiet:
                    print(box, ', confidence: ', self.out_scores[idx], 'ratio:', ratio, category_index[v]['name'])
                self.car_boxes.append(box)
        return self.car_boxes

frozen_graph = "/home/ubuntu/frozen_inference_graph.pb"
det = CarDetector(frozen_graph)

def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="")
    return graph

def find_box(image):
   # image =cv2.imread(img_file)
    graph = load_graph(frozen_graph)
    image_expanded = np.expand_dims(image, axis=0)
    image_tensor = graph.get_tensor_by_name('image_tensor:0')

    with tf.Session(graph=graph) as sess:
        # Note: we don't nee to initialize/restore anything
        # There is no Variables in this graph, only hardcoded constants
         (boxes, scores, classes, num_detections) = sess.run( (graph.get_tensor_by_name('detection_boxes:0'),
                                                               graph.get_tensor_by_name('detection_scores:0'),
                                                               graph.get_tensor_by_name('detection_classes:0'),
                                                               graph.get_tensor_by_name('num_detections:0')),
                                                             feed_dict = {image_tensor: image_expanded}
                                                            )

    return boxes, scores, classes, num_detections

def reduce_box(output_tensor):
    boxes, scores, classes, num_detections = output_tensor
    boxes = np.squeeze(boxes)
    scores = np.squeeze(scores)
    classes = np.squeeze(classes)
    valid_boxes = [box for i,box in enumerate(boxes) if classes[i]<9 and scores[i]>0.3]
    return len(valid_boxes)
