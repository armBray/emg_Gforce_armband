# from gforce import GForceProfile, NotifDataType, DataNotifFlags
from gforce import *
import time
import threading
import struct

def print_acceleration(data):
    acc_iter = struct.iter_unpack('<3l', data[1:])
    acceleration = []
    for i in acc_iter:
        acceleration.append(i)
    print('acceleration:', acceleration)

def print_gyroscope(data):
    gyro_iter = struct.iter_unpack('<3l', data[1:])
    gyroscope = []
    for i in gyro_iter:
        gyroscope.append(i)
    print('gyroscope:', gyroscope)

def print_magnetometer(data):
    magn_iter = struct.iter_unpack('<3l', data[1:])
    magnetometer = []
    for i in magn_iter:
        magnetometer.append(i)
    print('magnetometer:', magnetometer)

def print_euler(data):
    euler_iter = struct.iter_unpack('3f', data[1:])
    euler = []
    for i in euler_iter:
        euler.append(i)
    print('euler:', euler)

def print_quaternion(data):
    quat_iter = struct.iter_unpack('f', data[1:])
    quaternion = []
    for i in quat_iter:
        quaternion.append(i[0])
    print('quaternion:', quaternion)

# def print_rotation(data):

def print_emg(data):
    emg = data[1:]
    for i in range(16):
        emg_frame = list(struct.unpack('<8B',emg[8*i:8*i+8]))
        #print(emg_frame)
        data_to_print = []
        for j in emg_frame:
            data_to_print.append(j)
        print('byte:{0} data = {1}' .format(i, data_to_print))


def ondata(data):
    if len(data) > 0:
        # print('data.length = {0} \ncontent = {1}'.format(len(data), data))
        # print('data.length = {0}'.format(len(data)))
        print(data[0])
        if data[0] == NotifDataType['NTF_ACC_DATA']: print_acceleration(data)
        elif data[0] == NotifDataType['NTF_GYO_DATA']: print_gyroscope(data)
        elif data[0] == NotifDataType['NTF_MAG_DATA']: print_magnetometer(data)
        elif data[0] == NotifDataType['NTF_EULER_DATA']: print_euler(data)
        elif data[0] == NotifDataType['NTF_QUAT_FLOAT_DATA']: print_quaternion(data)
        # elif rotation
        elif data[0] == NotifDataType['NTF_EMG_ADC_DATA']: print_emg(data)

def set_cmd_cb(resp,raspData):
    print('Command result: {}'.format(resp))

def print2menu():
    print('_'*75)
    print('0: Exit')
    print('1: Get Accelerate')      #OK
    print('2: Get Gyroscope')       #OK
    print('3: Get Magnetometer')    #OK
    print('4: Get Euler')           #OK
    print('5: Get Quaternion')      #OK
    print('6: Get Rotation')        #tbd
    print('7: Get Raw EMG data')    #_
    print('8: Get others')

def main():
    while stop_main:
        GF = GForceProfile()
        # Scan all gforces,return [[num,dev_name,dev_addr,dev_Rssi,dev_connectable],...]
        scan_results = GF.scan(5)

        # Display the first menu
        print('_'*75)
        print('0: exit')

        if scan_results == []:
            print('No bracelet was found')
        else:
            for d in scan_results:
                print(
                    '{0:<1}: {1:^16} {2:<18} Rssi={3:<3}, connectable:{4:<6}'.format(*d))

        # Handle user actions
        button = int(
            input('Please select the device you want to connect or exit:'))
    
        if button == 0:
            break
        else:
            addr = scan_results[button-1][2]
            GF.connect(addr)

            # Display the secord menu
            while True:
                time.sleep(5)
                print2menu()
                button = int(input('Please select a function or exit:'))

                if button == 0:
                    break

                elif button == 1:
                    GF.setDataNotifSwitch(DataNotifFlags['DNF_ACCELERATE'], set_cmd_cb, 1000)
                    GF.startDataNotification(ondata)
                    
                    while True:
                        button = input()
                        if len(button) != 0:
                            GF.stopDataNotification()
                            GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 1000)
                            break
                
                elif button == 2:
                    GF.setDataNotifSwitch(DataNotifFlags['DNF_GYROSCOPE'], set_cmd_cb, 1000)
                    GF.startDataNotification(ondata)

                    while True:
                        button = input()
                        if len(button) != 0:
                            GF.stopDataNotification()
                            GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 1000)
                            break

                elif button == 3:
                    GF.setDataNotifSwitch(DataNotifFlags['DNF_MAGNETOMETER'], set_cmd_cb, 1000)
                    GF.startDataNotification(ondata)

                    while not KeyboardInterrupt:
                        # button = input()
                        # if len(button) != 0:
                        GF.stopDataNotification()
                        GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 1000)
                        break    

                elif button == 4:
                    GF.setDataNotifSwitch(DataNotifFlags['DNF_EULERANGLE'], set_cmd_cb, 1000)
                    GF.startDataNotification(ondata)

                    while True:
                        button = input()
                        if len(button) != 0:
                            GF.stopDataNotification()
                            GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 1000)
                            break     

                elif button == 5:
                    GF.setDataNotifSwitch(DataNotifFlags['DNF_QUATERNION'], set_cmd_cb, 1000)
                    GF.startDataNotification(ondata)

                    while True:
                        button = input()
                        if len(button) != 0:
                            GF.stopDataNotification()
                            GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 1000)
                            break  

                elif button == 6:
                    GF.setDataNotifSwitch(DataNotifFlags['DNF_ROTATIONMATRIX'], set_cmd_cb, 1000)
                    GF.startDataNotification(ondata)

                    while True:
                        button = input()
                        if len(button) != 0:
                            GF.stopDataNotification()
                            GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 1000)
                            break  

                elif button == 7:
                    GF.setDataNotifSwitch(DataNotifFlags['DNF_EMG_RAW'], set_cmd_cb, 1000)
                    time.sleep(2)
                    GF.startDataNotification(ondata)

                    while True:
                        button = int(input())
                        if button == 0:
                            GF.stopDataNotification()
                            GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 1000)
                            break  
                        # elif button == 5:
                        #     GF.stopDataNotification()
                        #     GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 1000)
                        #     time.sleep(8)
                        #     GF.setDataNotifSwitch(DataNotifFlags['DNF_EMG_RAW'], set_cmd_cb, 1000)
                        #     GF.startDataNotification(ondata)        
                        # else: print("input 0 or 5")                    

                elif button == 8:
                    GF.setDataNotifSwitch(0x08, set_cmd_cb, 1000) # 0x00000040    0x00000100  0x00000200  0x00000400  0x00000800  0xFFFFFFFF
                    GF.startDataNotification(ondata)

                    while True:
                        button = input()
                        if len(button) != 0:
                            GF.stopDataNotification()
                            GF.setDataNotifSwitch(DataNotifFlags['DNF_OFF'], set_cmd_cb, 1000)
                            break  


            break

if __name__ == '__main__':

    stop_main = True

    try:
        main()
    except KeyboardInterrupt:
        stop_main = False
        pass


