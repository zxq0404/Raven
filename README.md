# Raven

Raven stands for "Real-time Attentive Video Enhancement Network". It is inspired by the three-eyed raven in game of thrones, who has "a thousand eyes and one", and apparently sees everything. The three eyed raven is magic of course, but we are pretty good at using modern technology to do magic. The main idea is to use a distributed system on the cloud to handle multiple live camera streams, with objection detection algorithm to provide real-time analytics of the cameras streams to the users.

Raven is implemented by the following data pipeline:

![pipeline](https://github.com/zxq0404/Raven/blob/master/docs/Raven_pipeline.png)

In the "Camera" instances, the camera live video streams are break into frames and sent to a messaging broker system ZeroMQ queue, which sits on the "Broker" instance. The "Worker" instances, equiped with an objection detection algorithm on the TensorFlow framework, pulls the frames from the queue and applies transfer learning on these frames. The ZeroMQ queue thus serves as a load-balancer. The objection come out in order that they were generated, I wrote a heap "Dory" as a short term memory  (named after the character in "Finding Dory") to sort things out. After "Dory" the sorted results are saved to a SQLite database, i.e. long term memory. 

The sorted data is also sent to a webserver where real time analytics are presented along with the original frames. It looks like this:

![pipeline](https://github.com/zxq0404/Raven/blob/master/docs/Raven_demo.png)

The number of cars detected as a function of time are presented in the chart for three different cameras. The corresponding video stream with objection detection results (blue boxes around the cars) are shown in the video below, while clicking on the legends allows switching between different cameras. 

4 worker instances were used to monitor these three cameras in real time (i.e. no noticable delay to the user), with a cost of about $5 per camera per day. To scale the number of cameras, simply increase the number of worker instances.

## Folder Structure 

The folder structure are listed below:

├── docs                    # Documentation files 

├── src                     # Source files 

├── test                    # Tests

├── LICENSE

└── README.md

The bash file and source code for each type of instances are provided in the relevant folders.



