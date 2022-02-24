"""
@file kinematics.py
@brief This file is meant to handle all the kinematic calculations used to drive the robot arms.
"""

import pyb, utime
from ulab import numpy as np
from math import sin, cos, atan2


## Need to define the universe to z0 reference frame. This will be done using solidworks.
def fwd_kinematics(theta1, theta2, l1, l2, offset):
    d1 = 0
    d2 = offset
    alpha1 = 0
    alpha2 = 0
    start = utime.ticks_us()
    A1 = np.array([[cos(theta1), -sin(theta1)*cos(alpha1), sin(theta1)*sin(alpha1), l1*cos(theta1)],
                   [sin(theta1), cos(theta1)*cos(alpha1), -cos(theta1)*sin(alpha1), l1*sin(theta1)],
                   [0, sin(alpha1), cos(alpha1), d1],
                   [0, 0, 0, 1]])
    A2 = np.array([[cos(theta2), -sin(theta2)*cos(alpha2), sin(theta2)*sin(alpha2), l2*cos(theta2)],
                   [sin(theta2), cos(theta2)*cos(alpha2), -cos(theta2)*sin(alpha2), l2*sin(theta2)],
                   [0, sin(alpha2), cos(alpha2), d2],
                   [0, 0, 0, 1]])
    A12 = np.dot(A1,A2)
    P = np.array([[0],[0],[3],[1]])
    end_effector = np.dot(A12, P)
    end = utime.ticks_us()
    diff = utime.ticks_diff(end, start)
    print(end_effector)
    print('Elapsed Time: %4.2f microseconds' % (diff))

if __name__ == '__main__':
    fwd_kinematics(90, 0, 6, 3, -4)