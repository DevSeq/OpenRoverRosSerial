#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import roslib; roslib.load_manifest('wiimote')
import rospy
from wiimote.msg import State
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

leftwheel  = None
rightwheel = None
v_left = 0.0
v_right = 0.0

def SendDirection_left():
    forward = True
    if v_left < 0:
        forward = False

    leftwheel.write(BEGINNING + DIRECTION + str(int(forward == True)) + END)

def SendDirection_right():
    forward = True
    if v_right < 0:
        forward = False
    rightwheel.write(BEGINNING + DIRECTION + str(int(forward == True)) + END)

def SendVelocity():
    leftwheel.write(BEGINNING + VELOCITY + str(int(abs(v_left) * 10)) + END)
    rightwheel.write(BEGINNING + VELOCITY + str(int(abs(v_right) * 10)) + END)



def callback(data):
    if data.nunchuk_joystick_zeroed[0] > 0.1 or data.nunchuk_joystick_zeroed[1] > 0.1:
        v_left = data.nunchuk_joystick_zeroed[0] + K * data.nunchuk_joystick_zeroed[1]
        v_right = data.nunchuk_joystick_zeroed[0] - K * data.nunchuk_joystick_zeroed[1]
        SendDirection_left()
        SendDirection_right()
        SendVelocity()

def listener():
    leftwheel  = serial.Serial('/dev/ttyUSB0')  # open serial port
    rightwheel = serial.Serial('/dev/ttyUSB1')  # open serial port

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('OpenRover_Serial', anonymous=True)

    rospy.Subscriber('wiimote/state', State, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    print "Test!!"
    listener()



