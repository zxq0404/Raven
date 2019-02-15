import base64, zmq
import time
import numpy as np
import time

# We write a heap here to use as the short term memory.

def bubble_insert(array, number):
# Insert a new number into the fixed length heap. The smallest number is poped out.
    i = 0
    pop_num = array[-1]
    while number<array[i] and i<len(array)-1:
        i+=1
    array[i+1:] = array[i:-1]
    array[i]=number

    return pop_num

class Dory:
# A very lightweight prototype database in memory. Named after Dolly the goldfish with very short memory.
    def __init__(self, maxsize = 32):
        self.limit = maxsize
        self.record = dict()
# A buffer that saves the data. We want it to maintain a order sorted by the "counter" key
# but don't want to sort the dictionary every time. The maximum number of the dictionary is "maxsize".
        self.bookkeeper =dict()
        self.output = [None]*3

# A dictionary /that keeps track of the order of the buffer dictionary items.

    def look(self, meta_data, message):
# Read the meta data and the message (frame) and sort them by "counter".
        pop_num=0
        try:
            camera_name = meta_data["camera"]
            timestamp = meta_data["time"]
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

def feed():
    IP = "tcp://*:5558"
    target_IP = "tcp://10.0.0.6:5560"
    context = zmq.Context()
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.bind(IP)
    sender = context.socket(zmq.PUSH)
    sender.connect(target_IP)
# Initialize message receiving

    dory = Dory()
    while True:
        meta_data = consumer_receiver.recv_json()
        img_msg = consumer_receiver.recv()
# Receive and sort
        pop_num=dory.look(meta_data, img_msg)
        camera_name = meta_data['camera']
        if pop_num>0:
            timestamp, boxes, img_msg = dory.output
            counter = int(pop_num)

            new_meta = {'camera' : camera_name,
                    'counter':str(counter),
                    'boxes': boxes,
                    'time': timestamp}
# Forward to the front end
            zmq_socket.send_json(new_meta, flags=zmq.SNDMORE)
            zmq_socket.send(img_msg)

if __name__=="__main__":
    feed()
