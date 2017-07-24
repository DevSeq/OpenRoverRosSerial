#!/usr/bin/env python

import roslib; roslib.load_manifest('wiimote')
import rospy
from wiimote.msg import State
from geometry_msgs.msg import Twist

K = 0.75 * 2
pub = rospy.Publisher('openrover_twist', Twist)


def callback(data):
    if data.nunchuk_joystick_zeroed[0] > 0.1 or data.nunchuk_joystick_zeroed[1] > 0.1:
        msg = Twist()
        msg.linear.x = data.nunchuk_joystick_zeroed[0] + K * data.nunchuk_joystick_zeroed[1]  #left
        msg.linear.y = data.nunchuk_joystick_zeroed[0] - K * data.nunchuk_joystick_zeroed[1]  #right
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
