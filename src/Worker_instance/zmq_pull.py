import time
import zmq
import base64
import os

def consumer():
    IP = "tcp://10.0.0.9:5557"
    print('consumer started...Ingest images from ', IP)
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect(IP)
    receiving_dir = '/home/ubuntu/received/'
    if not os.path.exists(receiving_dir):
        os.makedirs(receiving_dir)
    i=0
    while True:
        i+=1
        meta_data = consumer_receiver.recv_json()
        saving_path = receiving_dir+meta_data['camera']+'_'+str(i)+'.jpg'
        message = consumer_receiver.recv()
        with open(saving_path, 'wb') as f:
            buff = base64.b64decode(message)
            f.write(buff)
        print(saving_path, "received and saved")

if __name__=="__main__":
    consumer()
