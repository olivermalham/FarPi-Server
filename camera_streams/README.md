# Marvin Streams
Mechanism for streaming video and sensor streams from Marvin.


### Data Source
Feed video data to Redis for further processing. Intention is to run the 
Redis server on the BrainCube, with any number of consumers doing stuff
like image recognition, depth analysis etc.


### Data Sink
Video_feed is a simple client that pushes a Marvin video feed from Redis to the
web.

### Tools
video_tools - Mixins for overlaying graphics on video feeds
marvin_feed - Mixin that handles the Redis side of things
marvin_array_feed - Mixin that builds on marvin_feed to handle Numpy arrays
marvin_feed_flask - Old way of feeding data from Realsense cameras to the web