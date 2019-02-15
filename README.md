# Raven

Raven stands for "Real-time Attentive Video Enhancement Network". It is inspired by the three-eyed raven in game of thrones, who has "a thousand eyes and one", and apparently sees everything. The three eyed raven is magic of course, but we are pretty good at using modern technology to do magic.

On one side, we have a lot of traffic cameras with live video streams, although most humans are probably disinterested in devoting their attention to these videos. On the other hand, computer vision has progressed a lot over the last few years, thanks to deep learning. For some jobs it may do better than human. So we can basically put 2 and 2 together and build Raven.

Raven is implemented by the following data pipeline:

![pipeline](https://github.com/zxq0404/Raven/blob/master/docs/Raven_pipeline.png)

In the "Camera" instances, the camera live video streams are break into frames and sent to a messaging system ZeroMQ queue, which is the "Streamer" instance. The "Worker" instances, equiped with an objection detection algorithm on the TensorFlow framework, pulls the frames from the queue and applies transfer learning on these frames. The ZeroMQ queue thus serves as a load-balancer. The objection detection results, along with the frames themselves, are sent to the "frontend" instance. Since the frames might not necessarily reach the front end in order that they were generated, I wrote a short term memory "Dory" (named after the character in "Finding Dory") to sort things out.

The sorted data is then sent to a webserver where real time analytics are presented along with the original frames. It looks like this:

![pipeline](https://github.com/zxq0404/Raven/blob/master/docs/Raven_demo.mp4)


## Folder Structure 

├── docs                    # Documentation files 

├── src                     # Source files 

├── test                    # Tests

├── LICENSE

└── README.md





