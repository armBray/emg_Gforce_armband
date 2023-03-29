#ifndef EMGSIGNALSIMULATOR_CLASS_H
#define EMGSIGNALSIMULATOR_CLASS_H
#include <iostream>
#include <string>
#include <vector>

#include "ros/ros.h"
#include <emg_signal_simulator_msgs/SetEmgSignal.h>
#include <emg_signal_simulator_msgs/SetEmgSignalwDuration.h>
#include <std_msgs/String.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Bool.h>

using namespace std;

namespace iiwa_ns
{
class emg_server_cls
{
public:
  emg_server_cls(ros::NodeHandle& nodeHandle, string TOPIC_PUB_NAME);

  int data, duration;
  string dataString;

  bool triggerData(emg_signal_simulator_msgs::SetEmgSignal::Request& req,
                   emg_signal_simulator_msgs::SetEmgSignal::Response& res);

  bool triggerState(emg_signal_simulator_msgs::SetEmgSignalwDuration::Request& req,
                    emg_signal_simulator_msgs::SetEmgSignalwDuration::Response& res);

  bool triggerVibrotactile(emg_signal_simulator_msgs::SetEmgSignal::Request& req,
                           emg_signal_simulator_msgs::SetEmgSignal::Response& res);

  string concatenateFunc();

  void test();

  virtual ~emg_server_cls();

private:
  ros::NodeHandle nodeHandle_;
  ros::ServiceServer service_;
  ros::ServiceServer trigger_state_service_;
  ros::ServiceServer vibro_service_;
  ros::Publisher publisher_;

  string SERVICE_NAME_ = "SetEmgSignal";
  string NODE_NAME_;
  string TOPIC_PUB_NAME_ = "";

  std_msgs::String msg;
};  // namespace iiwa_ns

/*
 * TO BE DEFINED IN CPP
 */
class emg_client_cls
{
public:
  emg_client_cls(ros::NodeHandle& nodeHandle, string var1, string var2);

  virtual ~emg_client_cls();

private:
  ros::NodeHandle nodeHandle_;
  ros::ServiceClient client_;
  // std_srvs::SetBool srv_;

  string terminalVar1_;
};

}  // namespace iiwa_ns

#endif
