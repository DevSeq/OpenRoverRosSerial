#!/usr/bin/env python

import roslib; roslib.load_manifest('wiimote')
import rospy
from geometry_msgs.msg import Twist
from vesc import Vesc





K = 0.75 / 2
scale = 5
v_left = 0.0
v_right = 0.0



def callback(data):
    global v_left
    old_left = v_left
    v_left  = (data.linear.x - K * data.linear.y)
    v_right = (data.linear.x + K * data.linear.y)

    diff = abs(old_left - v_left)

    if diff < 0.05:
        v_left = old_left

    if abs(v_left) >= 0.1 and abs(v_left) <= 0.90:
        print "v_l {0} ".format(v_left)
        vesc.setandmonitorPWM(v_left)



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



