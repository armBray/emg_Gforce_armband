cmake_minimum_required(VERSION 2.8.3)
project(emg_state_machine)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
  roslaunch
)

roslaunch_add_file_check(launch)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if you package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES lib
 CATKIN_DEPENDS message_runtime
#  DEPENDS system_lib
)


## mark examples for installation
install(DIRECTORY examples
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  USE_SOURCE_PERMISSIONS
  FILES_MATCHING PATTERN "*.py"
  PATTERN ".svn" EXCLUDE
)
