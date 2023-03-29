#!/usr/bin/env python3
import rospy
from std_msgs.msg import Header
from std_msgs.msg import String
from std_msgs.msg import Float32,Float64MultiArray
from ros_gforce.msg import EmgArray, ImuArray, Quaternion, Euler

from scipy import signal
from numpy import zeros
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import iir_filter
import rosbag

fs = 650.0  # Sample frequency (Hz)
f0 = 50.0  # Frequency to be removed from signal (Hz)
f1 = 60.0  # Frequency to be removed from signal (Hz)

sos1 = signal.butter(4, 324, 'lowpass', fs=650, output='sos')           #notch
high = signal.butter(4, f1, 'hp', fs=650, output='sos')  #high
iir1 = iir_filter.IIR_filter(sos1)
iir2 = iir_filter.IIR_filter(high)

single_c_pub = rospy.Publisher('data0', Float32, queue_size=10)
# pub2 = rospy.Publisher('data1', Float32, queue_size=10)
multi_c_pub = rospy.Publisher('datas3', Float64MultiArray, queue_size=10)
# bag = rosbag.Bag('test.bag', 'w')

# Initialize an empty list to store moving averages
to_ms = []
window_size = 130

def notch_high_abss(iir1, iir2, data):

    filtered2 = iir2.filter(iir1.filter(data))
    return abs(filtered2) * abs(filtered2)

def callback(data):
    global single_c_pub, window_size, to_ms, bag, multi_c_pub

    array = []
    mov_avg = []
    signal_ready = []

    signal_ready_np = np.asarray(signal_ready)
    
    for i in range(len(data.data)):
        # low_pass = iir1.filter(data.data[i])
        high_pass = iir2.filter(data.data[i])
        abs_square = abs(high_pass) * abs(high_pass)
        array.append(abs_square)

                        # print(array)
                        # s = Float64MultiArray()
                        # s.data = array
                        # # single_c_pub.publish(float(array[7]))
                        # multi_c_pub.publish(s)
                        
                        # single_c_pub.publish(float(abs_square))
    
    to_ms.append(array)
    # print(len(to_ms),len(to_ms[0]))
    # print(to_ms)
    to_ms_np = np.asarray(to_ms)
    # print(to_ms_np.shape)


                        ####################################### SINGLE CHANNEL
                        # if(len(to_ms) == window_size):
                        #     # rms = np.sqrt(np.mean(y**2))
                        #     mov_avg = np.sum(to_ms) / window_size
                        #     # single_c_pub.publish(float(total))

                        #     # to publish
                        #     signal_ready = np.sqrt(mov_avg)
                        #     single_c_pub.publish(float(signal_ready))

                        #     # to rosbag
                        #     # s = Float32()
                        #     # s.data = float(signal_ready)
                        #     # bag.write('chatter', s)

                        #     to_ms = []
                        #######################################
    for i in range(8):
        avg = np.mean(to_ms_np[:,i])
        # mov_avg = np.append(mov_avg, avg, axis=0)
    #     print('current average =', avg)
    #     print('readings used for average:', to_ms[:][i])
        top = np.sqrt(avg)
        # print(type(top))
        signal_ready = np.append(signal_ready, [np.sqrt(avg)], axis=0)
    # print(signal_ready.shape)
    print(np.size(to_ms_np,0))
    ####################################### MULTICHANNEL
    if(np.size(to_ms_np,0) == window_size):
        to_ms.pop(0)
        print("inside")
    #     for i in range(8):
    #         ma = np.sum(to_ms[:][i]) / window_size
    #         mov_avg.append(ma)
    #         signal_ready.append(np.sqrt(mov_avg[i]))
    #         # print(mov_avg)
    #         # single_c_pub.publish(float(mov_avg))
        s = Float64MultiArray()
        s.data = signal_ready
    #     # single_c_pub.publish(float(array[7]))
        multi_c_pub.publish(s)
    # #     # to publish
    # #     signal_ready = np.sqrt(mov_avg)
    # #     single_c_pub.publish(float(signal_ready))

    # #     # to rosbag
    # #     # s = Float32()
    # #     # s.data = float(signal_ready)
    # #     # bag.write('chatter', s)
        # to_ms.pop(0)
    
    #######################################


def listener():

    rospy.init_node('emg_filter_calibration', anonymous=True)
    rospy.Subscriber("/gf_emg", EmgArray, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    finally:
        # bag.close()
        print("Finish")