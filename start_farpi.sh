#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/usr/local/lib

echo "Starting Marvin FarPi service..."
python3 farpi.py marvin >> /var/log/marvin/farpi.log 2>&1

