#!/usr/bin/env python3
import rospy
from std_msgs.msg import String


def callback(data):
    print(data)

if __name__ == '__main__':

    global s_pub
    rospy.init_node('ciao', anonymous=True)
    rate = rospy.Rate(10) # ROS Rate at 5Hz

    sensordata_sub = rospy.Subscriber("/sensorsdata", String, callback)
    
    rospy.spin()
