#!/usr/bin/env python3
import rospy
from std_msgs.msg import Header
from std_msgs.msg import String
from ros_gforce.msg import Cc, cmInt8
from rospy_tutorials.msg import HeaderString
import message_filters
import json

########################
### Global Variables ###
########################
msg = String()

######################
### Synch Callback ###
######################
# def callback(sensordata_sub, cc_level, gripper_sub, compliance_sub):
def callback(sensordata_sub, cc_level, gripper_sub, compliance_sub,detect_sub,program_sub):
  # Solve all of perception here...
  # print("inside cb")
  global msg
  # msg = json.dumps({"cc_level_norm": sensordata_sub.data, "cc_level": cc_level.data, "gripper": gripper_sub.data, "compliance": compliance_sub.data})
  # msg = "{ 'cc_level_norm': " + sensordata_sub.data + ", 'cc_level': " + str(cc_level.data) + ", 'gripper': " + str(gripper_sub.data) +", 'compliance': " + str(compliance_sub.data) +"}"
  msg = "{ 'cc_level_norm': " + sensordata_sub.data + ", 'cc_level': " + str(cc_level.data) + ", 'gripper': " + str(gripper_sub.data) +", 'compliance': " + str(compliance_sub.data) +", 'detect': " + str(detect_sub.data) +", 'program': " + str(program_sub.data) +"}"
  # print(msg[19])
  # print(type(msg))
  # msg = sensordata_sub.data
  # msg = msg[19]
  print(msg)

############
### MAIN ###
############
if __name__ == '__main__':

  #########################
  ### Node's definition ###
  #########################
  global s_pub
  rospy.init_node('parse', anonymous=True)
  rate = rospy.Rate(10) # ROS Rate at 5Hz

  ##########################
  ### Sub/Pub definition ###
  ##########################
  sensordata_sub = message_filters.Subscriber("/sensordata_pub", HeaderString)
  cc_level = message_filters.Subscriber("/cc_level", Cc)
  gripper_sub = message_filters.Subscriber("/gripper_pub", cmInt8)
  compliance_sub = message_filters.Subscriber("/compliance_pub", cmInt8)
  detect_sub = message_filters.Subscriber("/detect_pub", cmInt8)
  program_sub = message_filters.Subscriber("/program_pub", cmInt8)
  s_pub = rospy.Publisher('sensorsdata', String)

  #############
  ### Synch ###
  #############
  # ts = message_filters.ApproximateTimeSynchronizer([sensordata_sub, cc_level, gripper_sub, compliance_sub], 10, 1)
  ts = message_filters.ApproximateTimeSynchronizer([sensordata_sub, cc_level, gripper_sub, compliance_sub,detect_sub,program_sub], 10, 1)
  ts.registerCallback(callback)

  while not rospy.is_shutdown():
      s_pub.publish(msg)
      rate.sleep()
