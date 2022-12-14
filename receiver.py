#!/usr/bin/env python

import rospy
import json
import time
from std_msgs.msg import String

def receiver(sent_msg):
    global direction_save
    data = json.loads(sent_msg.data)
    if data["Comment"] == "Flag : You achieved to spy ROS communication!":
        with open('log/test.log', 'a') as file:
            file.write('Message received - Acceleration : ' + str(data["Acceleration"]) + " - Direction : " + str(data["Direction"]) + " - Global Direction : " + str(direction_save) + "\n")
        direction_save = direction_save + data["Direction"]
        rospy.loginfo("Received")
    else:
        error.append(sent_msg)
        with open('log/test.log', 'a') as file:
            file.write('Message received == Error!! ==> ' + sent_msg)
        time.sleep(3)

if __name__ == '__main__':
    global direction_save
    global error
    error = []
    rospy.init_node("receiver", anonymous=True)
    rate = rospy.Rate(2)
    direction_save = 0
    subscribed = rospy.Subscriber(
            "sender", 
            String, 
            receiver,
            queue_size=1,
        )
    while not rospy.is_shutdown():
        rate.sleep()
