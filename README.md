# Raven

Raven stands for "Real-time Attentive Video Enhancement Network". It is inspired by the three-eyed raven in game of thrones, who has "a thousand eyes and one", and apparently sees everything. The three eyed raven is magic of course, but we are pretty good at using modern technology to do magic.

On one side, we have a lot of traffic cameras with live video streams, although most humans are probably disinterested in paying attention to these videos. On the other hand, computer vision has progressed a lot over the last few years, and for some jobs it may do better than human. So we can basically put 2 and 2 together and build Raven, a computer network that applies deep learning computer vision algorithm at scale, and provides real time analytics to the users.

Raven is implemented by the following data pipeline:

![pipeline](https://github.com/zxq0404/Raven/blob/master/docs/Raven_pipeline.png)

In the "Camera" instances, the camera live video streams are break into frames and sent to a messaging broker system ZeroMQ queue, which sits on the "Broker" instance. The "Worker" instances, equiped with an objection detection algorithm on the TensorFlow framework, pulls the frames from the queue and applies transfer learning on these frames. The ZeroMQ queue thus serves as a load-balancer. The objection come out in order that they were generated, I wrote a heap "Dory" as a short term memory  (named after the character in "Finding Dory") to sort things out. After "Dory" the sorted results are saved to a SQLite database, i.e. long term memory. 

The sorted data is also sent to a webserver where real time analytics are presented along with the original frames. It looks like this:

![pipeline](https://github.com/zxq0404/Raven/blob/master/docs/Raven_demo.png)

The number of cars as a function of time are presented in the chart for three different cameras. The corresponding video with objection detection results (blue boxes around the cars) are shown in the video below. Clicking on the legend to switch between different cameras.


## Folder Structure 

├── docs                    # Documentation files 

├── src                     # Source files 

├── test                    # Tests

├── LICENSE

└── README.md





