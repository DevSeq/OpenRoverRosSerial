#!/usr/bin/env python

import roslib; roslib.load_manifest('wiimote')
import rospy
from geometry_msgs.msg import Twist
import serial

BEGINNING = 'B',
VELOCITY = 'V',
PWM = 'P',
GAINS = 'G',
CURRENT = 'C',
START = 'S',
DIRECTION = 'D',
READ = 'R',
WRITE = 'W',
END = '\n',

K = 0.75 * 2

left_wheel  = None
right_wheel = None
v_left = 0.0
v_right = 0.0


def send_direction_left():
    forward = True
    if v_left < 0:
        forward = False

    left_wheel.write(BEGINNING + DIRECTION + str(int(forward == True)) + END)


def send_direction_right():
    forward = True
    if v_right < 0:
        forward = False
    right_wheel.write(BEGINNING + DIRECTION + str(int(forward == True)) + END)


def send_velocity():
    left_wheel.write(BEGINNING + VELOCITY + str(int(abs(v_left) * 10)) + END)
    right_wheel.write(BEGINNING + VELOCITY + str(int(abs(v_right) * 10)) + END)


def callback(data):
        global v_left
        global v_right
        v_left = data.x
        v_right = data.y
        send_direction_left()
        send_direction_right()
        send_velocity()


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



