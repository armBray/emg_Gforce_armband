cmake_minimum_required(VERSION 2.8.3)
project(emg_signal_simulator_msgs)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  message_generation
)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  SetEmgSignal.srv
  SetEmgSignalwDuration.srv
)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
)

###################################
## catkin specific configuration ##
###################################

catkin_package(
  CATKIN_DEPENDS message_runtime
)
