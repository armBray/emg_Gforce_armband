/*
 * rosserial Publisher Example
 * Prints "hello world!"
 */

#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Empty.h>

std_msgs::String str_msg;

ros::NodeHandle  nh;
ros::Publisher motor_state("motor_state", &str_msg);

void messageVibroDetect( const std_msgs::Empty& on_msg){
    digitalWrite(3, HIGH);   // on motor
    delay(800);
    digitalWrite(3, LOW);   // off motor
    
    str_msg.data = "Detect";
    motor_state.publish( &str_msg );
}

void messageVibroProgram( const std_msgs::Empty& on_msg){
    digitalWrite(3, HIGH);   // on motor
    delay(200);
    digitalWrite(3, LOW);   // off motor
    delay(200);
    digitalWrite(3, HIGH);   // on motor
    delay(200);
    digitalWrite(3, LOW);   // off motor
    delay(200);
    
    str_msg.data = "Program";
    motor_state.publish( &str_msg );
}

void messageVibroGripper( const std_msgs::Empty& off_msg){
    digitalWrite(3, HIGH);  
    delay(200);
    digitalWrite(3, LOW);  
    
    str_msg.data = "Gripper";
    motor_state.publish( &str_msg );
}

void messageVibroCompliance( const std_msgs::Empty& off_msg){
    digitalWrite(3, HIGH);  
    delay(200);
    digitalWrite(3, LOW);   
    delay(100);
    digitalWrite(3, HIGH);  
    delay(800);
    digitalWrite(3, LOW);  
    
    str_msg.data = "Compliance";
    motor_state.publish( &str_msg );
}

ros::Subscriber<std_msgs::Empty> vibro_detect("on_vibro_detect", &messageVibroDetect );
ros::Subscriber<std_msgs::Empty> vibro_program("on_vibro_program", &messageVibroProgram );
ros::Subscriber<std_msgs::Empty> vibro_gripper("on_vibro_gripper", &messageVibroGripper );
ros::Subscriber<std_msgs::Empty> vibro_compliance("on_vibro_compliance", &messageVibroCompliance );

char hello[13] = "hello world!";

void setup()
{
  pinMode(3, OUTPUT);
  nh.initNode();
  nh.advertise(motor_state);
  nh.subscribe(vibro_detect);
  nh.subscribe(vibro_program);
  nh.subscribe(vibro_gripper);
  nh.subscribe(vibro_compliance);
}

void loop()
{
  //str_msg.data = hello;
  //motor_state.publish( &str_msg );
  nh.spinOnce();
  delay(1000);
}
