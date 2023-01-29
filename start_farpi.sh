#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/usr/local/lib

# python3 ./streamer/streamer.py 5001 1 >> ./log/camera1_stream.log 2>&1 &
# python3 ./streamer/streamer.py 5002 2 >> ./log/camera2_stream.log overlay 2>&1 &

echo "Starting Marvin FarPi service..."
python3 farpi.py marvin >> /var/log/marvin/farpi.log 2>&1

