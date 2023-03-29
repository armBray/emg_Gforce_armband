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
import yaml
from yaml.loader import SafeLoader
import sys

p_inv_list = []
k_list = []
cc_range = []

fs = 650.0  # Sample frequency (Hz)
f0 = 50.0  # Frequency to be removed from signal (Hz)
f1 = 60.0  # Frequency to be removed from signal (Hz)

sos1 = signal.butter(4, 324, 'lowpass', fs=650, output='sos')           #notch
high = signal.butter(4, f1, 'hp', fs=650, output='sos')  #high
iir1 = iir_filter.IIR_filter(sos1)
iir2 = iir_filter.IIR_filter(high)

single_c_pub = rospy.Publisher('data0', Float32, queue_size=10)
cc_level_pub = rospy.Publisher('cc_level', Float32, queue_size=10)
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
    
    to_ms.append(array)
    # print(len(to_ms),len(to_ms[0]))
    # print(to_ms)
    to_ms_np = np.asarray(to_ms)
    # print(to_ms_np.shape)

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
        s = Float64MultiArray()
        s.data = signal_ready
        multi_c_pub.publish(s)

    mat_mult = np.matmul(p_inv_list, signal_ready)
    print("mat_mult: ", mat_mult)
    print(type(mat_mult))
    # print(mat_mult[0][0])
    # print(mat_mult[1][0])
    a = np.array([mat_mult[0]/k_list[0][0], mat_mult[1]/k_list[0][1]])
    print("a: ", a)
    print(type(a))

    cc_level = a.min()
    print("cc_level: ", cc_level)
    print(type(cc_level))
    
    cc = Float32()
    # cc.data = (cc_level - cc_range[0][1]) / (cc_range[0][0] - cc_range[0][1])
    # cc.data = (cc_level - cc_range[0][1]) / cc_range[0][0]
    # cc.data = (cc_level - cc_range[0][1]) #NO
    # cc.data = (cc_level - cc_range[0][0]) #NO
    # cc.data = cc_level
    cc.data = (cc_level - 0) / 20000
    cc_level_pub.publish(cc)


def listener():

    rospy.init_node('emg_filter_cc_level', anonymous=True)
    rospy.Subscriber("/gf_emg", EmgArray, callback)
    
    rospy.spin()


if __name__ == '__main__':
    try:
        yaml_imp_file = sys.argv[1] + '_matrix.yaml'
        # Open the file and load the file
        # yaml_path = '~/Escritorio/armband_ws/src/ros_gforce/yaml/' + yaml_imp_file
        with open(yaml_imp_file) as f:
            yaml_data = yaml.load(f, Loader=SafeLoader)
            # print(yaml_data)

        for key, value in yaml_data.items():
            if key == "cc_level_min" or key == "cc_level_max":
                # print(value)
                cc_range.append(value)
            elif key == "k_ext" or key == "k_flex":
                # print(value)
                k_list.append(value)
                # k_list = np.append(k_list, value, axis=0)
            else:
                p_inv_list = np.append(p_inv_list, value, axis=0)

        cc_range = np.array(cc_range)
        print(type(cc_range))
        print(cc_range.shape)
        cc_range = np.reshape(cc_range,(1,2))

        k_list = np.array(k_list)
        print(type(k_list))
        print(k_list.shape)
        k_list = np.reshape(k_list,(1,2))

        print(k_list.shape)
        print(k_list)

        p_inv_list = np.reshape(p_inv_list,(2,8))
        print(p_inv_list)
        print(type(p_inv_list))
        listener()

    finally:
        # bag.close()
        print("Finish")