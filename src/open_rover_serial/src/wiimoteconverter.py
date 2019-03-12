#!/usr/bin/env python

import roslib; roslib.load_manifest('wiimote')
import rospy
import math
from wiimote.msg import State
from geometry_msgs.msg import Twist

pub = rospy.Publisher('openrover_twist', Twist, queue_size=10)


def callback(data):
    if abs(data.nunchuk_joystick_zeroed[0]) > 0.0001 or abs(data.nunchuk_joystick_zeroed[1]) > 0.0001:
        msg = Twist()
        msg.linear.x = data.nunchuk_joystick_zeroed[1]
        msg.linear.y = data.nunchuk_joystick_zeroed[0]
        print "x {0} y {1} ".format(msg.linear.x, msg.linear.y)
        pub.publish(msg)


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Wiimote_converter', anonymous=True)

    rospy.Subscriber('wiimote/state', State, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    print "wiimote converter Test!!"
    listener()
