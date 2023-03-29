#!/usr/bin/env python3
import rospy
from std_msgs.msg import Header
from std_msgs.msg import String
from std_msgs.msg import Float32
from ros_gforce.msg import EmgArray, ImuArray, Quaternion, Euler

from scipy import signal
from numpy import zeros
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import iir_filter

fs = 650.0  # Sample frequency (Hz)
f0 = 50.0  # Frequency to be removed from signal (Hz)
Q = 5.0  # Quality factor
# Design notch filter
b, a = signal.iirnotch(f0, Q, fs)

#####################################################  PLOT FILTER
# Frequency response
# freq, h = signal.freqz(b, a, fs=fs)
# Plot
# fig, ax = plt.subplots(2, 1, figsize=(8, 6))
# ax[0].plot(freq, 20*np.log10(abs(h)), color='blue')
# ax[0].set_title("Frequency Response")
# ax[0].set_ylabel("Amplitude (dB)", color='blue')
# ax[0].set_xlim([0, 100])
# ax[0].set_ylim([-25, 10])
# ax[0].grid(True)
# ax[1].plot(freq, np.unwrap(np.angle(h))*180/np.pi, color='green')
# ax[1].set_ylabel("Angle (degrees)", color='green')
# ax[1].set_xlabel("Frequency (Hz)")
# ax[1].set_xlim([0, 100])
# ax[1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
# ax[1].set_ylim([-90, 90])
# ax[1].grid(True)
# plt.show()
##################################################

pub = rospy.Publisher('chatter', Float32, queue_size=10)

window_size = 130
i = 0

# Initialize an empty list to store moving averages
to_filter = []
filtered = []


def callback(data):
    global a,b,noisySignal,pub, i , window_size, to_filter, filtered

    ###############################   PROVA CON FILTFILT -> NEED ARRAY
    # waveData = np.array([data.data[0],data.data[0]], dtype='u8')
    # outputSignal = signal.filtfilt(b, a, waveData, padlen=0)
    # sos = signal.butter(15, 20, 'hp', fs=650, output='sos')
    # filtered = signal.sosfilt(sos, outputSignal)
    # abs_square = abs(filtered) * abs(filtered)
    # to_filter.append(abs_square)
    # print(len(to_filter))

    # if(len(to_filter) == 200):
    #     # print(type(abs_square))
    #     # print(abs_square)
    #     # rms = np.sqrt(np.mean(y**2))
    #     total = np.sum(to_filter) / 200
    #     total = np.sqrt(total)
    #     pub.publish(float(total))
    #     to_filter = []
    ################################

    # f0 = 48.0
    # f1 = 52.0
    # sos1 = signal.butter(4, [f0/fs*2,f1/fs*2], 'bandstop', output='sos')
    sos1 = signal.butter(4, 50/650*2, output='sos')
    high = signal.butter(4, 20/650*2, 'highpass', output='sos')
    iir1 = iir_filter.IIR_filter(sos1)
    iir2 = iir_filter.IIR_filter(high)

    # filtered = iir1.filter(data.data[0])
    filtered2 = iir2.filter(iir1.filter(data.data[7]))
    # pub.publish(float(filtered2))

    abs_square = abs(filtered2) * abs(filtered2)
    pub.publish(float(abs_square))

    # to_filter.append(abs_square)
    # print(len(to_filter))

    # if(len(to_filter) == window_size):
    #     # rms = np.sqrt(np.mean(y**2))
    #     total = np.sum(to_filter) / window_size
    #     # pub.publish(float(total))

    #     total = np.sqrt(total)
    #     pub.publish(float(total))
    #     to_filter = []


def listener():

 
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/gf_emg", EmgArray, callback)
    
    rospy.spin()

if __name__ == '__main__':
    listener()