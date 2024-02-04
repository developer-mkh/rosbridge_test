#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import pigpio
from std_msgs.msg import Int16

GPIO_PIN = 19

pi = pigpio.pi()
pi.set_mode(GPIO_PIN, pigpio.OUTPUT)

def callback(msg):
    p_out = msg.data
    pi.write(GPIO_PIN, p_out)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/led', Int16, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
