*** LINK UTILI ***

http://wiki.ros.org/rosserial_arduino/Tutorials
https://www.youtube.com/watch?v=0QJmaV8c39w&list=PLud1D2wIGgfphDMApXHoUfPnOWbciQ1Mc
https://www.youtube.com/watch?v=lkyUqMVJBQ0

*** USAGE ***
roscore
dmesg -> find for tty
rosrun rosserial_python serial_node.py /dev/ttyACM0
rostopic echo /motor_state 
rostopic pub /on_motor std_msgs/Empty "{}"
rostopic pub /off_motor std_msgs/Empty "{}"

*** USAGE W/ EMG SIMULATOR & STATE MACHINE ***
roslaunch emg_signal_simulator EmgSignalSimulator_class_node.launch 
rosrun rosserial_python serial_node.py /dev/ttyACM0
roslaunch emg_state_machine emg_state_machine.launch 
rosservice call /EmgSignalSimulator_class_node/SetEmgSignalwDuration "state: 'gripper'" 

*** FINAL ***
SET CONNECTION ETHERNET
rosrun rosserial_python serial_node.py /dev/ttyACM0
rosrun plotjuggler plotjuggler
RUN MATLAB
roslaunch emg_state_machine emg_state_machine.launch 


*** gforce usage ***
bluetoothctl
connect 24:71:89:F0:52:77

find /usr/local/lib -name bluepy-helper
sudo setcap cap_net_raw+e      /usr/local/lib/python3.8/dist-packages/bluepy/bluepy-helper
sudo setcap cap_net_admin+eip  /usr/local/lib/python3.8/dist-packages/bluepy/bluepy-helper

rosrun ros_gforce prova_pub.py


*** 



