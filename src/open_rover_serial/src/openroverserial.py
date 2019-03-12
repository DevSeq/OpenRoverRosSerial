#!/usr/bin/env python

import roslib; roslib.load_manifest('wiimote')
import rospy
from geometry_msgs.msg import Twist
from vesc import Vesc
import time






K = 0.75 / 2
scale = 5
v_left = 0.0
v_right = 0.0
current_time = 0

def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def callback(data):
    global v_left
    global v_right
    global current_time
    old_time = current_time
    old_left = v_left
    old_right = v_right
    v_left  = (data.linear.x - K * data.linear.y)
    v_right = (data.linear.x + K * data.linear.y)

    v_left  = clamp(v_left,  -0.5,0.5)
    v_right = clamp(v_right, -0.5,0.5)


    current_time = time.clock() #time.process_time()
    delta_t = abs(current_time - old_time)
    if abs(v_left) > 0.05 and  abs(v_right) > 0.05:
        print "v_l {0} ".format(v_left)
        print "v_r {0} ".format(v_right)
        vesc.setandmonitorPWM(v_left, v_right)
    elif delta_t > 0.1:
        vesc.setandmonitorPWM(0.0, 0.0)
    elif v_left < 0.01 and v_right < 0.01:
        vesc.setandmonitorPWM(0.0, 0.0)



def listener():
    global vesc
    vesc = Vesc()
    vesc.findandmapcontrollers()
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('OpenRover_Serial', anonymous=True)
    rospy.Subscriber('openrover_twist', Twist, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    print "Test!!"
    listener()



