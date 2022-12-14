FROM ros:noetic-ros-core

RUN mkdir /home/ros && mkdir /home/ros/log
COPY receiver.py /home/ros/
