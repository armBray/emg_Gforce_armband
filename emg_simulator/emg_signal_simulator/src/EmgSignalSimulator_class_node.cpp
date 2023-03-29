#include <ros/ros.h>
#include <string>
#include "emg_signal_simulator/EmgSignalSimulator_class.hpp"

int main(int argc, char** argv)
{
  ros::init(argc, argv, "EmgSignalSimulator_node");
  ROS_INFO("Successfully launched node: %s.", ros::this_node::getName().c_str());

  ros::NodeHandle nodeHandle("~");
  // ros::NodeHandle nodeHandle;

  ROS_INFO("Ready to trigger data.");
  ros::Rate r(stoi(argv[1]));  // 10 hz
  iiwa_ns::emg_server_cls emg_server_cls(nodeHandle, argv[2]);

  ros::Publisher sensorpublisher_ = nodeHandle.advertise<std_msgs::String>("/sensorsdata", 1);
  ros::Publisher vibropublisher_ = nodeHandle.advertise<std_msgs::String>("/vibrotactiledata", 1);
  std_msgs::String msg;

  int i = 0;
  while (ros::ok())
  {
    // emg_server_cls.test();
    if (emg_server_cls.data == 1 && i < emg_server_cls.duration)
    {
      msg.data = "1";
      sensorpublisher_.publish(msg);
      i++;
    }
    else
    {
      i = 0;
      emg_server_cls.data = 0;
      msg.data = "0";
      sensorpublisher_.publish(msg);
    }
    if (emg_server_cls.dataString == "vibro1")
    {
      msg.data = "vibro1";
      vibropublisher_.publish(msg);
      i++;
    }
    else if (emg_server_cls.dataString == "vibro2")
    {
      msg.data = "vibro2";
      vibropublisher_.publish(msg);
      i++;
    }
    ros::spinOnce();  // WARNING Do not put ros::spin();
    r.sleep();
  }

  return 0;
}
