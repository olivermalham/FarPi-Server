#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/usr/local/lib

echo "Starting Skuttle FarPi service..."
python3 farpi.py skuttle >> /var/log/skuttle/farpi.log 2>&1

cd streams/flask/
python3 video_stream_flask.py 8889 0 2 >> /var/log/skuttle/video_stream.log 2>&1

