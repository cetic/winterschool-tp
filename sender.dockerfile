FROM ros:noetic-ros-core

RUN mkdir /home/ros && mkdir /var/log/ros
COPY sender.py /home/ros/
