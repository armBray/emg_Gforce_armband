#!/usr/bin/env python

import rospy
import smach
import smach_ros
from smach import CBState
from std_msgs.msg import Empty
from std_msgs.msg import String
from std_msgs.msg import Float64,Float32
from std_msgs.msg import Int8
from std_msgs.msg import Header
from rospy_tutorials.msg import HeaderString
from emg_state_machine_msgs.msg import vectorString, cmInt8, cmFloat32
import sys

counter = 0
my_data = None
rate = 0
tag_order = []
flag_dictionary = {"Init": True, "Detect": True, "Program": True, "Gripper": True, "Compliance": True}

def RunOnceFactory():
    class RunOnceBase(object): # abstract base class
        _shared_state = {} # shared state of all instances (borg pattern)
        has_run = False
        def __init__(self, *args, **kwargs):
            self.__dict__ = self._shared_state
            if not self.has_run:
                self.stuff_done_once(*args, **kwargs)
                self.has_run = True
    return RunOnceBase

def msg_constructor(msg_data, type):

    h = Header()
    h.stamp = rospy.Time.now()
    h.frame_id = ''

    if type == "HeaderString":
        msg = HeaderString()
        msg.header = h
        msg.data = msg_data
    elif type == "cmInt8":
        msg = cmInt8()
        msg.header = h
        msg.data = int(msg_data)
    else:
        # print('msg_constructor not detect type of message', file = sys.stderr)
        print('msg_constructor not detect type of message')
    return msg

# define state Init
class Init(smach.State):
    global rate,tag_order,flag_dictionary

    def __init__(self,sensordata_pub,sensordata_tag_pub,status_pub,vector_tag_pub,my_data,gripper_pub,compliance_pub):
        smach.State.__init__(self, outcomes=['initLoop','detect'])
        self.sensordata_pub = sensordata_pub
        self.sensordata_tag_pub = sensordata_tag_pub
        self.status_pub = status_pub
        self.vector_tag_pub = vector_tag_pub
        self.gripper_pub = gripper_pub
        self.compliance_pub = compliance_pub
        self.my_data = my_data
        self.counter_init = 0
        print("flag_dictionary :", flag_dictionary)

    class once(RunOnceFactory()):
        def stuff_done_once(self, *args, **kwargs):
            print("MyFunction1.stuff_done_once() called")
            tag_order.append('NORMAL')

    def execute(self, userdata):
        Init.once()
        rospy.loginfo('Executing state Init')
        # global counter,rate
        rospy.loginfo("Inside execute %s", my_data)
        msg = '0'
        self.sensordata_pub.publish(msg_constructor(msg,"HeaderString"))
        self.gripper_pub.publish(msg_constructor(msg,"cmInt8"))
        self.compliance_pub.publish(msg_constructor(msg,"cmInt8"))

        tag_msg = 'NORMAL'
        self.sensordata_tag_pub.publish(tag_msg)

        rospy.loginfo('counter_init %s', self.counter_init)
        if flag_dictionary['Init']:
            status_msg = 'WAITING TRIGGER'
            self.status_pub.publish(status_msg)
            # for x in tag_order:
            # vector_tag_msg = x
            self.vector_tag_pub.publish(tag_order)
            flag_dictionary['Init'] = False
        rate.sleep()
        # if my_data == '1':
        if my_data > 0.5:
            self.counter_init += 1
            if self.counter_init > 14 :
                print(tag_order)
                flag_dictionary['Detect'] = True
                self.counter_init = 0
                return 'detect'
            return 'initLoop'
        else:
            self.counter_init = 0
            return 'initLoop'

class Detect(smach.State):
    def __init__(self,sensordata_pub,sensordata_tag_pub,status_pub,vibro_detect_pub,gripper_pub,compliance_pub,vibro_program_pub):
        smach.State.__init__(self, outcomes=['detectLoop','program'])
        self.sensordata_pub = sensordata_pub
        self.sensordata_tag_pub = sensordata_tag_pub
        self.status_pub = status_pub
        self.counter_detect = 0
        self.vibro_detect_pub = vibro_detect_pub
        self.gripper_pub = gripper_pub
        self.compliance_pub = compliance_pub
        self.vibro_program_pub = vibro_program_pub


    def execute(self, userdata):
        rospy.loginfo('Executing state Detect')
        global rate
        if self.counter_detect < 1 :
            self.vibro_detect_pub.publish()
        self.counter_detect += 1
        rospy.loginfo('counter_detect %s', self.counter_detect)
        msg = '0'
        self.sensordata_pub.publish(msg_constructor(msg,"HeaderString"))
        self.gripper_pub.publish(msg_constructor(msg,"cmInt8"))
        self.compliance_pub.publish(msg_constructor(msg,"cmInt8"))
        tag_msg = 'NORMAL'
        self.sensordata_tag_pub.publish(tag_msg)
        rate.sleep()
        # if self.counter_detect > 20 and flag_dictionary['Detect']:
        #     status_msg = 'SET VALUE TO PROGRAM'
        #     self.status_pub.publish(status_msg)
        #     flag_dictionary['Detect'] = False
        # # if self.counter_detect > 20 and my_data == '1':
        # if self.counter_detect > 20 and my_data > 0.5:
        #     self.counter_detect = 0
        #     return 'program'
        # else:
        #     return 'detectLoop'
        # if self.counter_detect > 20 and flag_dictionary['Detect']:
        #     status_msg = 'SET VALUE TO PROGRAM'
        #    self.status_pub.publish(status_msg)
        #     flag_dictionary['Detect'] = False
        if my_data < 0.5:
            self.counter_detect = 0
            self.vibro_program_pub.publish()
            return 'program'
        else:
            return 'detectLoop'

# define state Program
class Program(smach.State):
    def __init__(self,sensordata_pub,sensordata_tag_pub,status_pub,vibro_compliance_pub,gripper_pub,compliance_pub):
        smach.State.__init__(self, outcomes=['program_GRIPPER','program_COMPLIANCE','programLoop','transition'])
        self.sensordata_pub = sensordata_pub
        self.sensordata_tag_pub = sensordata_tag_pub
        self.vibro_compliance_pub = vibro_compliance_pub
        self.gripper_pub = gripper_pub
        self.compliance_pub = compliance_pub
        self.status_pub = status_pub
        self.counter_program = 0

    def execute(self, userdata):
        global rate, my_data, counter
        flag_dictionary['Init'] = True
        rospy.loginfo('Executing state Program')
        # counter += 1
        self.counter_program += 1
        rospy.loginfo('Counter %s', counter)
        msg = '0'
        self.sensordata_pub.publish(msg_constructor(msg,"HeaderString"))
        self.gripper_pub.publish(msg_constructor(msg,"cmInt8"))
        self.compliance_pub.publish(msg_constructor(msg,"cmInt8"))
        tag_msg = 'NORMAL'
        self.sensordata_tag_pub.publish(tag_msg)
        rate.sleep()

        # if my_data == '0' and counter == 5:
        # if my_data < 0.5 and counter == 5:
        #     return 'program_GRIPPER'
        # elif counter < 15 and counter == 14:
        #     self.vibro_compliance_pub.publish()
        #     return 'program_COMPLIANCE'
        # else:
        #     return 'programLoop'


        # if my_data > 0.5:
        #     self.counter_program += 1
        #     if my_data < 0.5 and self.counter_program == 5:
        #         return 'program_GRIPPER'
        #     elif my_data < 0.5 and self.counter_program < 15 and self.counter_program == 14:
        #         self.vibro_compliance_pub.publish()
        #         return 'program_COMPLIANCE'
        #     else:
        #         self.counter_program = 0
        #         return 'programLoop'
        # else:
        #     self.counter_program = 0
        #     return 'programLoop'

        if self.counter_program > 20 and flag_dictionary['Program']:
            status_msg = 'SET VALUE TO TRANSITION'
            self.status_pub.publish(status_msg)
            flag_dictionary['Program'] = False
        # if self.counter_detect > 20 and my_data == '1':
        if self.counter_program > 20 and my_data > 0.5:
            self.counter_program = 0
            return 'transition'
        else:
            return 'programLoop'

# define state Transition
class Transition(smach.State):
    def __init__(self,sensordata_pub,sensordata_tag_pub,status_pub,vibro_compliance_pub,gripper_pub,compliance_pub):
        smach.State.__init__(self, outcomes=['program_GRIPPER','program_COMPLIANCE','transitionLoop'])
        self.sensordata_pub = sensordata_pub
        self.sensordata_tag_pub = sensordata_tag_pub
        self.vibro_compliance_pub = vibro_compliance_pub
        self.gripper_pub = gripper_pub
        self.compliance_pub = compliance_pub
        self.status_pub = status_pub
        self.counter_transition = 0

    def execute(self, userdata):
        global counter, rate, my_data
        flag_dictionary['Init'] = True
        rospy.loginfo('Executing state Transition')
        counter += 1
        rospy.loginfo('Counter %s', counter)
        msg = '0'
        self.sensordata_pub.publish(msg_constructor(msg,"HeaderString"))
        self.gripper_pub.publish(msg_constructor(msg,"cmInt8"))
        self.compliance_pub.publish(msg_constructor(msg,"cmInt8"))
        tag_msg = 'NORMAL'
        self.sensordata_tag_pub.publish(tag_msg)
        rate.sleep()

        # if my_data == '0' and counter == 5:
        if my_data < 0.5 and counter == 5:
            return 'program_GRIPPER'
        elif counter < 15 and counter == 14:
            self.vibro_compliance_pub.publish()
            return 'program_COMPLIANCE'
        else:
            return 'transitionLoop'

# define state Gripper
class Gripper(smach.State):
    def __init__(self,sensordata_pub,sensordata_tag_pub,status_pub,vibro_gripper_pub,gripper_pub,compliance_pub):
        smach.State.__init__(self, outcomes=['gripperLoop','gotoInit'])
        self.sensordata_pub = sensordata_pub
        self.sensordata_tag_pub = sensordata_tag_pub
        self.status_pub = status_pub
        self.counter_gripper_pub = 0
        self.vibro_gripper_pub = vibro_gripper_pub
        self.gripper_pub = gripper_pub
        self.compliance_pub = compliance_pub

    def execute(self, userdata):
        global counter, rate
        # rate = rospy.Rate(50)
        rospy.loginfo('Executing state Gripper')
        # call to service here
        self.gripperPub()
        counter = 0
        self.counter_gripper_pub += 1
        rate.sleep()

        if self.counter_gripper_pub == 5:
            self.counter_gripper_pub = 0
            tag_order.append('GRIPPER')
            print(tag_order)
            status_msg = 'VALUE SET TO GRIPPER'
            self.status_pub.publish(status_msg)
            self.vibro_gripper_pub.publish()
            # rospy.Duration(1)
            # status_msg = 'INIT'
            # self.status_pub.publish(status_msg)
            return 'gotoInit'
        else:
            return 'gripperLoop'

    def gripperPub(self):
        rospy.loginfo('*** gripperPub ***')
        msg = '1'
        self.sensordata_pub.publish(msg_constructor(msg,"HeaderString"))
        self.gripper_pub.publish(msg_constructor(msg,"cmInt8"))
        self.compliance_pub.publish(msg_constructor('0',"cmInt8"))
        tag_msg = 'GRIPPER'
        self.sensordata_tag_pub.publish(tag_msg)


# define state Compliance
class Compliance(smach.State):
    def __init__(self,sensordata_pub,sensordata_tag_pub,status_pub,vibro_compliance_pub,gripper_pub,compliance_pub):
        smach.State.__init__(self, outcomes=['complianceLoop','gotoInit'])
        self.sensordata_pub = sensordata_pub
        self.sensordata_tag_pub = sensordata_tag_pub
        self.status_pub = status_pub
        self.counter_compliance_pub = 0
        self.vibro_compliance_pub = vibro_compliance_pub
        self.gripper_pub = gripper_pub
        self.compliance_pub = compliance_pub

    def execute(self, userdata):
        global counter, rate
        rospy.loginfo('Executing state Compliance')
        # call to service here
        self.compliancePub()
        counter = 0
        self.counter_compliance_pub += 1
        rate.sleep()

        if self.counter_compliance_pub == 15:
            self.counter_compliance_pub = 0
            tag_order.append('COMPLIANCE')
            print(tag_order)
            status_msg = 'VALUE SET TO COMPLIANCE'
            self.status_pub.publish(status_msg)
            # self.vibro_compliance_pub.publish()
            # status_msg = 'INIT'
            # self.status_pub.publish(status_msg)
            return 'gotoInit'
        else:
            return 'complianceLoop'

    def compliancePub(self):
        rospy.loginfo('*** compliancePub ***')
        msg = '1'
        self.sensordata_pub.publish(msg_constructor(msg,"HeaderString"))
        self.compliance_pub.publish(msg_constructor(msg,"cmInt8"))
        self.gripper_pub.publish(msg_constructor('0',"cmInt8"))
        tag_msg = 'COMPLIANCE'
        self.sensordata_tag_pub.publish(tag_msg)


@smach.cb_interface(input_keys=[],
                    output_keys=[],
                    outcomes=['publishing'])
def Normal_cb(ud):
    global counter, data
    rate = rospy.Rate(10)
    rospy.loginfo('Normal_cb')
    my_cb_topic = rospy.Publisher('/sensordatadfg', Int8, queue_size=1)
    counter_topic = rospy.Publisher('/counter', Int8, queue_size=1)
    msg = 1
    my_cb_topic.publish(msg)
    counter = counter + 1
    counter_topic.publish(counter)
    rate.sleep()
    if counter > 125 :
        counter = 0

    return 'publishing'

def callback(data):
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        global my_data
        my_data = data.data

# main
def main():

    rospy.init_node('emg_state_machine')

    # Get Parameters
    # rate_param = rospy.get_param("/emg_state_machine/rate")

    sensorsdata_sub = rospy.Subscriber('/cc_level', cmFloat32, callback)
    sensordata_pub = rospy.Publisher('/sensordata_pub', HeaderString, queue_size=1)
    sensordata_tag_pub = rospy.Publisher('/sensordata_tag_pub', String, queue_size=1)
    status_pub = rospy.Publisher('/status_pub', String, queue_size=1)
    vector_tag_pub = rospy.Publisher('/vector_tag_pub', vectorString, queue_size=1)
    gripper_pub = rospy.Publisher('/gripper_pub', cmInt8, queue_size=1)
    compliance_pub = rospy.Publisher('/compliance_pub', cmInt8, queue_size=1)
    vibro_detect_pub = rospy.Publisher('/on_vibro_detect', Empty, queue_size=1)
    vibro_program_pub = rospy.Publisher('/on_vibro_program', Empty, queue_size=1)
    vibro_gripper_pub = rospy.Publisher('/on_vibro_gripper', Empty, queue_size=1)
    vibro_compliance_pub = rospy.Publisher('/on_vibro_compliance', Empty, queue_size=1)

    global rate, my_data
    rate = rospy.Rate(10)
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=[])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('INIT', Init(sensordata_pub,sensordata_tag_pub,status_pub,vector_tag_pub,sensorsdata_sub,gripper_pub,compliance_pub),
                               transitions={'initLoop':'INIT',
                                            'detect':'DETECT'})
        smach.StateMachine.add('DETECT', Detect(sensordata_pub,sensordata_tag_pub,status_pub,vibro_detect_pub,gripper_pub,compliance_pub,vibro_program_pub),
                               transitions={'detectLoop':'DETECT',
                                            'program':'PROGRAM'})
        smach.StateMachine.add('PROGRAM', Program(sensordata_pub,sensordata_tag_pub,status_pub,vibro_compliance_pub,gripper_pub,compliance_pub),
                               transitions={'programLoop':'PROGRAM',
                                            'program_GRIPPER':'GRIPPER',
                                            'program_COMPLIANCE':'COMPLIANCE',
                                            'transition':'TRANSITION'})
        smach.StateMachine.add('TRANSITION', Transition(sensordata_pub,sensordata_tag_pub,status_pub,vibro_compliance_pub,gripper_pub,compliance_pub),
                               transitions={'transitionLoop':'TRANSITION',
                                            'program_GRIPPER':'GRIPPER',
                                            'program_COMPLIANCE':'COMPLIANCE'})
        smach.StateMachine.add('GRIPPER', Gripper(sensordata_pub,sensordata_tag_pub,status_pub,vibro_gripper_pub,gripper_pub,compliance_pub),
                               transitions={'gripperLoop':'GRIPPER',
                                            'gotoInit':'INIT'})
        smach.StateMachine.add('COMPLIANCE', Compliance(sensordata_pub,sensordata_tag_pub,status_pub,vibro_compliance_pub,gripper_pub,compliance_pub),
                               transitions={'complianceLoop':'COMPLIANCE',
                                            'gotoInit':'INIT'})
        smach.StateMachine.add('MY_CB', CBState(Normal_cb),
                                {'publishing':'MY_CB'})

    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Execute SMACH plan
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    # rospy.spin()
    sis.stop()

if __name__ == '__main__':
    main()