#include <ros/ros.h>
#include "emg_signal_simulator/EmgSignalSimulator_class.hpp"

using namespace std;

namespace iiwa_ns
{
/***********************
 *** emg_server_cls ***
 ************************/

emg_server_cls::emg_server_cls(ros::NodeHandle& nodeHandle, string TOPIC_PUB_NAME)
  : nodeHandle_(nodeHandle), TOPIC_PUB_NAME_(TOPIC_PUB_NAME)
{
  NODE_NAME_ = ros::this_node::getName();
  ROS_INFO("Constructor 'emg_server_cls' called...in  %s.", NODE_NAME_.c_str());
  service_ = nodeHandle_.advertiseService(SERVICE_NAME_, &emg_server_cls::triggerData, this);
  trigger_state_service_ = nodeHandle_.advertiseService("SetEmgSignalwDuration", &emg_server_cls::triggerState, this);
  vibro_service_ = nodeHandle_.advertiseService("Setvibro", &emg_server_cls::triggerVibrotactile, this);
  ROS_INFO("Service GetTrajFromDB advertised...");

  ROS_INFO("Defining publisher...");
  publisher_ = nodeHandle_.advertise<std_msgs::String>(TOPIC_PUB_NAME, 1);

  string s = emg_server_cls::concatenateFunc();
  bool prova = ros::service::exists(s, true);
}

bool emg_server_cls::triggerData(emg_signal_simulator_msgs::SetEmgSignal::Request& req,
                                 emg_signal_simulator_msgs::SetEmgSignal::Response& res)
{
  ROS_INFO("inside callback emg_server_cls::triggerData");
  if (req.data == "0")
  {
    ROS_INFO("***");
    ROS_INFO("***");
    ROS_INFO("***");
    res.success = true;
    res.message = "set to 0";
    msg.data = "0";
  }
  else if (req.data == "1")
  {
    ROS_INFO("***");
    ROS_INFO("***");
    ROS_INFO("***");
    res.success = true;
    res.message = "set to 1";
    msg.data = "1";
  }
  else if (req.data == "0.5")
  {
    ROS_INFO("***");
    ROS_INFO("***");
    ROS_INFO("***");
    res.success = true;
    res.message = "set to 0.5";
    msg.data = "0.5";
  }
  else if (req.data == "badtrigger")
  {
    ROS_INFO("***");
    ROS_INFO("***");
    ROS_INFO("***");
    res.success = true;
    res.message = "set to badtrigger";
    msg.data = "badtrigger";
  }
  else if (req.data == "goodtrigger")
  {
    ROS_INFO("***");
    ROS_INFO("***");
    ROS_INFO("***");
    res.success = true;
    res.message = "set to goodtrigger";
    msg.data = "goodtrigger";
  }
  else
  {
    ROS_INFO("***");
    ROS_INFO("***");
    ROS_INFO("***");
    res.success = false;
    res.message = "Please enter a valid value: 0,1 or 0.5";
  }
  // publisher_.publish(msg);
  // ROS_INFO_STREAM(res);
  return true;
}

bool emg_server_cls::triggerState(emg_signal_simulator_msgs::SetEmgSignalwDuration::Request& req,
                                  emg_signal_simulator_msgs::SetEmgSignalwDuration::Response& res)
{
  ROS_INFO("inside callback emg_server_cls::triggerState");
  if (req.state == "gripper")
  {
    data = 1;
    duration = 5;
    res.success = true;
    res.message = "set to 1 for 0.5 sec";
  }
  else if (req.state == "compliance")
  {
    data = 1;
    duration = 15;
    res.success = true;
    res.message = "set to 1 for 1.5 sec";
  }
  else if (req.state == "badtrigger")
  {
    data = 1;
    duration = 2;
    res.success = true;
    res.message = "set to 1 for 0.2 sec";
  }
  else if (req.state == "goodtrigger")
  {
    data = 1;
    duration = 5;
    res.success = true;
    res.message = "set to 1 for 0.5 sec";
  }

  return true;
}

bool emg_server_cls::triggerVibrotactile(emg_signal_simulator_msgs::SetEmgSignal::Request& req,
                                         emg_signal_simulator_msgs::SetEmgSignal::Response& res)
{
  ROS_INFO("inside callback emg_server_cls::triggerVibrotactile");
  if (req.data == "vibro1")
  {
    dataString = "vibro1";
    res.success = true;
    res.message = "set vibro1";
  }
  else if (req.data == "vibro2")
  {
    dataString = "vibro2";
    res.success = true;
    res.message = "set vibro2";
  }

  return true;
}

string emg_server_cls::concatenateFunc()
{
  std::string s;
  s.append(NODE_NAME_);
  s.append("/");
  s.append(SERVICE_NAME_);
  return s;
}

void emg_server_cls::test()
{
  publisher_.publish(msg);
  ROS_INFO_STREAM(msg);
}

emg_server_cls::~emg_server_cls()
{
}

/***********************
 *** emg_client_cls ***
 ************************/

}  // namespace iiwa_ns
