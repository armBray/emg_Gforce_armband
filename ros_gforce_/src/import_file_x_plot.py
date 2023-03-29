#!/usr/bin/env python3
import pandas as pd
import numpy as np
from nmf import NMF
import yaml
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import math
import sys

######################
### YAML functions ###
######################

def yaml_loader(filepath):          # Loads a yaml file
     with open(filepath, 'r') as file_descriptor:
          data = yaml.load(file_descriptor)
     return data

def yaml_dump(filepath, data):      # Dumps data to a yaml file
      with open(filepath, 'w') as file_descriptor:
          yaml.dump(data, file_descriptor)


##################
### CSV import ###
##################

csv_name = sys.argv[1] # Format -> num_name -> 0_Armando
print("Opening csv -> " + csv_name + '.csv')
csv_path = '~/Escritorio/armband_ws/src/ros_gforce/csv/' + csv_name + '.csv'
# data = pd.read_csv(r'~/Escritorio/armband_ws/sec.csv')
data = pd.read_csv(csv_path)
df = pd.DataFrame(data)
# print(df)

time = df["%time"]
ch0 = df["field.data0"]
ch1 = df["field.data1"]
ch2 = df["field.data2"]
ch3 = df["field.data3"]
ch4 = df["field.data4"]
ch5 = df["field.data5"]
ch6 = df["field.data6"]
ch7 = df["field.data7"]
print("time: ", len(time))

(c,r) = df.transpose().shape
A = np.zeros((8,r))
print(A.shape)

A[0][:] = ch0.transpose()
A[1][:] = ch1.transpose()
A[2][:] = ch2.transpose()
A[3][:] = ch3.transpose()
A[4][:] = ch4.transpose()
A[5][:] = ch5.transpose()
A[6][:] = ch6.transpose()
A[7][:] = ch7.transpose()

time_t = np.arange(0, r, 1, dtype=int)
# print(time_t.shape)
# print(A[0][:].shape)


###############################
### Parameters' computation ###
###############################

print("Computation nnmf...")
# M, U_Offline, info = NMF().run(A[:,windows_index[0][0]:windows_index[1][0]], 2)
model = NMF(n_components=2, init='random', max_iter = 1000, random_state=0)
M = model.fit_transform(A)
U_Offline = model.components_

print(M)
print("M shape: ", M.shape)
print("M type: ", type(M))

print("U_Offline shape: ", U_Offline.shape)
print("U_Offline type: ", type(U_Offline))


U_Offline_T = U_Offline.transpose()
print(U_Offline_T)
print("U_Offline_T size: ",U_Offline_T.shape)
print("U_Offline_T type: ",type(U_Offline_T))

print("Computation M pinv...")

M_pinv = np.linalg.pinv(M)
print(M_pinv.tolist())
print("M_pinv: ", M_pinv.shape)

print("Defining vectors...")

u_ext = U_Offline_T[0][:]
u_flex = U_Offline_T[1][:]
print("u_ext type:", type(u_ext))
print("u_ext type:", len(u_ext))

# k_ext =  np.sum(U_Offline_T[0][:]) / diff_range_index
# k_flex = np.sum(U_Offline_T[1][:]) / diff_range_index
# print(type(k_ext))
# print(k_ext)
# k_ext = float(k_ext)
# k_flex = float(k_flex)
# print(type(k_ext))
# print(k_ext)


############
### Plot ###
############

# plt.plot(A[0][:])
# plt.show()

### U_Offline
# fig_uoff, ax_uoff = plt.subplots()
# fig_uoff.suptitle('U_Offline')
# ax_uoff.plot(time_t, U_Offline[0][:], label='u_ext')
# ax_uoff.plot(time_t, U_Offline[1][:], label='u_flex')
# ax_uoff.set_xlabel('samples')
# ax_uoff.legend()

### CHANNELS SEPARATE
# plt.figure(1)
# plt.suptitle('channel filtered')
# plt.subplot(4, 2, 1)
# plt.plot(time_t, A[0][:])
# plt.subplot(4, 2, 2)
# plt.plot(time_t, A[1][:])
# plt.subplot(4, 2, 3)
# plt.plot(time_t, A[2][:])
# plt.subplot(4, 2, 4)
# plt.plot(time_t, A[3][:])
# plt.subplot(4, 2, 5)
# plt.plot(time_t, A[4][:])
# plt.subplot(4, 2, 6)
# plt.plot(time_t, A[5][:])
# plt.subplot(4, 2, 7)
# plt.plot(time_t, A[6][:])
# plt.subplot(4, 2, 8)
# plt.plot(time_t, A[7][:])
# plt.show()


# fig_emg_f_rms, axes_emg_f_rms = plt.subplots(4,2)
# fig_emg_f_rms.suptitle('EMG filtered RMS')

# axes_emg_f_rms[0,0].plot(time_t, A[0][:], label='ch1')
# axes_emg_f_rms[0,0].set_ylabel('ch1')
# axes_emg_f_rms[1,0].plot(time_t, A[1][:], label='ch2')
# axes_emg_f_rms[1,0].set_ylabel('ch2')
# axes_emg_f_rms[2,0].plot(time_t, A[2][:], label='ch3')
# axes_emg_f_rms[2,0].set_ylabel('ch3')
# axes_emg_f_rms[3,0].plot(time_t, A[3][:], label='ch4')
# axes_emg_f_rms[3,0].set_ylabel('ch4')

# axes_emg_f_rms[0,1].plot(time_t, A[4][:], label='ch5')
# axes_emg_f_rms[0,1].set_ylabel('ch5')
# axes_emg_f_rms[1,1].plot(time_t, A[5][:], label='ch6')
# axes_emg_f_rms[1,1].set_ylabel('ch6')
# axes_emg_f_rms[2,1].plot(time_t, A[6][:], label='ch7')
# axes_emg_f_rms[2,1].set_ylabel('ch7')
# axes_emg_f_rms[3,1].plot(time_t, A[7][:], label='ch8')
# axes_emg_f_rms[3,1].set_ylabel('ch8')

# axes_emg_f_rms[3,0].set_xlabel('samples')
# axes_emg_f_rms[3,1].set_xlabel('samples')

# plt.show()


### CHANNEL JOINT + SELECT RANGE
# plt.figure(2)
fig = plt.figure(3)
fig.suptitle('channel filtered together')
ax = fig.subplots()
for i in range(8):
    ax.plot(time_t, A[i][:], label= "ch " + str(i+1))
fig.legend(title='channels:')

# Defining the cursor
cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True,
                color = 'r', linewidth = 1)

# Creating an annotating box
annot = ax.annotate("", xy=(0,0), xytext=(-40,40),textcoords="offset points",
                    bbox=dict(boxstyle='round4', fc='linen',ec='k',lw=1),
                    arrowprops=dict(arrowstyle='-|>'))
annot.set_visible(False)

# Function for storing and showing the clicked values
coord = []
def onclick(event):
    global coord
    coord.append((event.xdata, event.ydata))
    x = event.xdata
    y = event.ydata
    
    # printing the values of the selected point
    print([x,y]) 
    annot.xy = (x,y)
    text = "({:.2g}, {:.2g})".format(x,y)
    annot.set_text(text)
    annot.set_visible(True)
    fig.canvas.draw() #redraw the figure
    
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()



# Unzipping the coord list in two different arrays
x1, y1 = zip(*coord)
print(x1, y1)
print(type(x1))

x1_np = []

for i in x1:
    x1_np = np.append(x1_np,math.trunc(i))

print(type(x1_np))

############
### YAML ###
############

write_range = { 'window_range' : x1_np.tolist()}
# write_k = {"k_ext": k_ext, "k_flex": k_flex}
res = {idx + 1 : M_pinv.tolist()[idx] for idx in range(len(M_pinv.tolist()))}
print(write_range)
print(type(write_range))


# filepath = "range.yaml"
range_yaml = sys.argv[1] + '_range'
print("writing yaml on -> " + range_yaml + '.yaml')
yaml_path = '/home/110682@TRI.LAN/Escritorio/armband_ws/src/ros_gforce/config/' + range_yaml + '.yaml'
# yaml_path = range_yaml + '.yaml'

with open(yaml_path, 'w') as file_descriptor:
    yaml.dump(write_range, file_descriptor)
    # yaml.dump(write_k, file_descriptor)
    # yaml.dump(res, file_descriptor)

