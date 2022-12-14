#FROM ubuntu:latest
FROM ros:noetic-ros-core

# Install SSH
RUN apt update && apt -y install ssh 
RUN mkdir /run/sshd

# Create user ws and provide sudo rights
RUN useradd -m -p $(perl -e 'print crypt($ARGV[0], "password")' 'WS_pwd2022') -s /bin/bash ws
RUN usermod -aG sudo ws

# Install nano, ettercap, network basic tools, python3.9, boofuzz
RUN apt update && apt -y install sudo nano ettercap-text-only iputils-ping python3-pip tcpdump nmap python3.9
RUN pip install boofuzz
RUN . /opt/ros/noetic/setup.sh && python3.9 -m pip install fuzzingbook==1.1 grammar

# Copy custom scripts and adapt privileges
COPY boofuzz.py /home/ws/test_boofuzz.py
RUN chown ws:ws /home/ws/test_boofuzz.py && chmod +x /home/ws/test_boofuzz.py
COPY ettercap.sh /home/ws/
COPY Rachel.py /home/ws
COPY Rachel.sh /home/ws
COPY grammar.py /home/ws
RUN chown ws:ws /home/ws/ettercap.sh /home/ws/Rachel.py /home/ws/Rachel.sh /home/ws/grammar.py && chmod +x /home/ws/ettercap.sh /home/ws/Rachel.sh
