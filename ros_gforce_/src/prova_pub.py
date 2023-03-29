#!/usr/bin/env python3
from gforce import GForceProfile, NotifDataType, DataNotifFlags, NotifDataLength
import time
import numpy as np
import rospy
from std_msgs.msg import Header
from ros_gforce.msg import EmgArray, ImuArray, Quaternion, Euler
import struct


def onData(data):
    ''' According to https://oymotion.github.io/gForceSDK/gForceSDK/
        unpack data from different notifications
    '''
    print('{0}  {1}'.format(data[0],len(data)))
    if data[0] == NotifDataType['NTF_ACC_DATA']:
        # 4 byte signed long
        acc = data[1:]
        h = Header()
        h.stamp = rospy.Time.now()
        h.frame_id = 'gf_acc'
        acc_frame = struct.unpack('<3l', acc)
        print(acc_frame)
                
        # Wrap the Accelerometer data into an ImuArray message
        acc_msg = ImuArray()
        acc_msg.header = h
        acc_msg.data = acc_frame
        accPub.publish(acc_msg)
    
    elif data[0] == NotifDataType['NTF_EULER_DATA']:
        euler = data[1:]
        h = Header()
        h.stamp = rospy.Time.now()
        h.frame_id = 'gf_euler'
        euler_frame = struct.unpack('3f', euler)
        
        # Wrap the Quaterion data into an Euler message
        euler_msg = Euler()
        euler_msg.header = h
        euler_msg.data = euler_frame
        eulerPub.publish(euler_msg)

    elif data[0] == NotifDataType['NTF_QUAT_FLOAT_DATA']:
        quat = data[1:]
        h = Header()
        h.stamp = rospy.Time.now()
        h.frame_id = 'gf_quat'
        quat_frame = struct.unpack('4f', quat)

        # Wrap the Quaternion data into a Quaternion message
        quat_msg = Quaternion()
        quat_msg.header = h
        quat_msg.data = quat_frame
        quatPub.publish(quat_msg)

    #elif data[0] == NotifDataType['NTF_EMG_ADC_DATA'] and len(data) == NotifDataLength['NTF_EULER_LEN'] + 1:
    elif data[0] == NotifDataType['NTF_EMG_ADC_DATA'] and len(data) == 129:

        emg = data[1:]
        for i in range(16):
        # for i in range(2):
            # rospy.logerr('aaaaaaaaaaa %d', i)
            h = Header()
            h.stamp = rospy.Time.now()
            h.frame_id = 'gf_emg_' + str(i)
            # h.frame_id = 'gf_emg_'
            emg_frame = list(struct.unpack('<8B',emg[8*i:8*i+8])) # the data type of the EMG samples is uint8_t
            # emg_frame = list(struct.unpack('<8B',emg[8:8+8]))

            # Wrap the EMG data into an EmgArray message
            emg_msg = EmgArray(h,emg_frame)
            emgPub.publish(emg_msg) 


def set_cmd_cb(resp,respdata):
    print('Command result: {}'.format(resp))

if __name__ == '__main__':

    # Config Emg Raw Data
    # channel_mask = 0xFF
    # data_len = 128
    # samp_rate = rospy.get_param("~sample_rate", 500)
    # resolution = rospy.get_param("~resolution", 8)

    channel_mask = 0xFF
    data_len = 128
    samp_rate = 500
    resolution = 8

    #---    topic definition
    acc_topic = rospy.get_param("~acc_topic", "gf_acc")
    euler_topic = rospy.get_param("~euler_topic", "gf_euler")
    quat_topic = rospy.get_param("~quat_topic", "gf_quat")
    emg_topic = rospy.get_param("~emg_topic", "gf_emg")

    #---    device connection
    connected = 0
    while(connected==0):
        GF = GForceProfile()
        print('Scanning....')
        scan_results = GF.scan(5.0)
        if scan_results != []:
            try:
                addr = scan_results[0][2]
                print(addr)
                GF.connect(addr)  
                #GF.setEmgRawDataConfig(sampRate = 1000 , channelMask = 0xFF, dataLen = 128, resolution = 8, cb=set_cmd_cb, timeout=1000)  
                connected = 1

            except (ValueError,KeyboardInterrupt) as e:
                print("gForce bracelet not found. Attempting to connect...")
                rospy.sleep(0.5)
                continue

    #--- node inizialization
    rospy.init_node('gf_pub_node')
    rospy.loginfo('node initialized...')

    #--- Define the gforce publisher
    rospy.loginfo('defining publishers...')
    accPub = rospy.Publisher(acc_topic, ImuArray, queue_size=1000)
    eulerPub = rospy.Publisher(euler_topic, Euler, queue_size=1000)
    quatPub = rospy.Publisher(quat_topic, Quaternion, queue_size=10000)
    emgPub = rospy.Publisher(emg_topic, EmgArray, queue_size=10000) # queue_size is set to 20 to guarantee the sampling rate
    rospy.loginfo('publishers defined...')


    # GF.setDataNotifSwitch(DataNotifFlags['DNF_ACCELERATE'],set_cmd_cb,2000)
    # GF.setDataNotifSwitch(DataNotifFlags['DNF_EULERANGLE'],set_cmd_cb,2000)
    # GF.setDataNotifSwitch(DataNotifFlags['DNF_QUATERNION'], set_cmd_cb, 1000)
    GF.setDataNotifSwitch(DataNotifFlags['DNF_EMG_RAW'], set_cmd_cb, 10000)

    # GF.setDataNotifSwitch(DataNotifFlags['DNF_ACCELERATE'] | DataNotifFlags['DNF_QUATERNION'] | DataNotifFlags['DNF_EULERANGLE'],set_cmd_cb,2000)

    try:
        GF.startDataNotification(onData) # startDataNotification gets one data packet, and uses ondata function to publish once
        rospy.spin()
    except (rospy.ROSInterruptException,KeyboardInterrupt) as e:
        print(e)
        rospy.loginfo("Disconnecting...")
        GF.stopDataNotification()
        rospy.loginfo("stopDataNotification...")
        GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 2000)
        rospy.loginfo("setDataNotifSwitch...")
        GF.disconnect()
        rospy.loginfo("disconnect...")
