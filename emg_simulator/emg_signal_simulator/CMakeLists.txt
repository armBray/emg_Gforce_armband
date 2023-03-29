cmake_minimum_required(VERSION 2.8.3)
project(emg_signal_simulator)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  emg_signal_simulator_msgs
)

###################################
## catkin specific configuration ##
###################################

catkin_package(
  INCLUDE_DIRS include
  CATKIN_DEPENDS roscpp
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
 include
 ${catkin_INCLUDE_DIRS}
)

add_executable(EmgSignalSimulator_class_node
  src/EmgSignalSimulator_class_node.cpp
  src/EmgSignalSimulator_class.cpp)
target_link_libraries(EmgSignalSimulator_class_node ${catkin_LIBRARIES})
# add_dependencies(EmgSignalSimulator_class_node emg_signal_simulator_gencpp)

add_executable(EmgSignalSimulator_class_client_node
  src/EmgSignalSimulator_class_client_node.cpp
  src/EmgSignalSimulator_class.cpp)
target_link_libraries(EmgSignalSimulator_class_client_node ${catkin_LIBRARIES})
# add_dependencies(EmgSignalSimulator_class_client_node emg_signal_simulator_gencpp)

# #############
# ## Install ##
# #############

install(TARGETS EmgSignalSimulator_class_node EmgSignalSimulator_class_client_node RUNTIME DESTINATION
  ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch/ DESTINATION
  ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

