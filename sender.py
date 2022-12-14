#!/usr/bin/env python

import rospy
import json
import random
from std_msgs.msg import String

def sender():
    #pub = rospy.Publisher('sender', String, queue_size=1)
    #rospy.init_node('sender', anonymous=True)
    accel = random.randint(0, 256)
    turning = random.randint(-100, 100)
    comment = "Flag : You achieved to spy ROS communication!"
    data = {"Acceleration": accel, "Direction": turning, "Comment": comment}
    pub.publish(json.dumps(data))
    #rospy.loginfo("Sent")

if __name__ == '__main__':
    pub = rospy.Publisher('sender', String, queue_size=1)
    rospy.init_node('sender', anonymous=True)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        try:
            sender()
        except rospy.ROSInterruptException:
            pass
        rate.sleep()
