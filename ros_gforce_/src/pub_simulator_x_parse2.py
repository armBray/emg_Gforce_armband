#!/usr/bin/env python3
import rospy
from std_msgs.msg import Header
from std_msgs.msg import String
from std_msgs.msg import Float32,Float64MultiArray, Int8
from ros_gforce.msg import EmgArray, ImuArray, Quaternion, Euler, Cc, Hs
from rospy_tutorials.msg import HeaderString
import json

if __name__ == '__main__':

    gripper_pub = rospy.Publisher("/gripper_pub", Cc, queue_size=10)
    compliance_pub = rospy.Publisher("/compliance_pub", HeaderString, queue_size=10)
    rospy.init_node('pub2', anonymous=True)
    rate = rospy.Rate(40) # ROS Rate at 5Hz

    msg = Cc()
    hs = HeaderString()

    while not rospy.is_shutdown():
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "cc"
        msg.data = 0.123

        hs.header.stamp = rospy.Time.now()
        hs.header.frame_id = "cc"
        hs.data = "0"
        
        gripper_pub.publish(msg)
        compliance_pub.publish(hs)
        rate.sleep()
    # listener()
