export WORKER=ubuntu@ec2-34-239-152-41.compute-1.amazonaws.com

source activate amazonei_tensorflow_p36

pip install zmq

pip install opencv-python

scp -i ~/.ssh/xiaoqingzhou-IAM-keypair.pem frozen_inference_graph.pb $WORKER:frozen_inference_graph.pb

scp -i ~/.ssh/xiaoqingzhou-IAM-keypair.pem dummy.jpg $WORKER:dummy.jpg
