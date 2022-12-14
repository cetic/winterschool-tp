#!/bin/bash

export ROS_MASTER_URI=http://ros-master:11311
source /opt/ros/noetic/setup.bash
python3.9 Rachel.py -t sender -r 10 -g 5
#python3.9 Rachel.py -t sender -r 10 -f -s 10
#python3.9 Rachel.py -t sender -r 10 -m "{\"Acceleration\": 152, \"Direction\": -93, \"Comment\": \"Flag : You achieved to spy ROS communication!}" -s 10
