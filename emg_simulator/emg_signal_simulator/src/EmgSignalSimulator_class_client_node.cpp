
#include <string>

#include <ros/ros.h>
#include "emg_signal_simulator/EmgSignalSimulator_class.hpp"

int main(int argc, char** argv)
{
  ros::init(argc, argv, "EmgSignalSimulator_client_node");
  if (argc != 3)
  {
    ROS_INFO("usage: EmgSignalSimulator_client arg1 arg2");
    ROS_INFO("where:");
    ROS_INFO("- arg1 -> string");
    ROS_INFO("- arg2 -> string");
    ROS_INFO("Successfully launched node: %s.", ros::this_node::getName().c_str());
    return 1;
  }

  ros::NodeHandle nodeHandle("~");
  // ros::NodeHandle nodeHandle;

  ros::spin();

  return 0;
}
