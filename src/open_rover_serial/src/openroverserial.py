#!/usr/bin/env python

import roslib; roslib.load_manifest('wiimote')
import rospy
from geometry_msgs.msg import Twist
import serial, time, numpy
from packets import Packet
import packets


K = 0.75 / 2
scale = 5

left_wheel  = None
right_wheel = None
v_left = 0.0
v_right = 0.0



def callback(data):
        global v_left
        global v_right
        v_left  = scale * (data.linear.x - K * data.linear.y)
        v_right = scale * (data.linear.x + K * data.linear.y)
        print "v_l {0} v_r {1} v{2} w{3}".format(v_left, v_right, data.linear.x, data.linear.y)


def listener():
    global left_wheel
    global right_wheel

    left_wheel  = serial.Serial('/dev/ttyACM0')  # open serial port
    right_wheel = serial.Serial('/dev/ttyACM1')  # open serial port

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



