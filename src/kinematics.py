''' @file           kinematics.py
    @brief          Finds initial angles necessary for xy coordinates
    @details        Using dynamic analyses from ME 423, we used the Denavit-
                    Hartenburg method to set up matrices for each joint. From
                    here, we multiply each joints' frame together to get the
                    final position and orientation of the end effector, in 
                    which case is the laser engraver. We then set the x and y
                    coordinates and use our inverse kinematic analyses to find
                    the necessary angles for our subsequent laser position.
                    
    @author         Jeremy Baechler
    @author         Kendall Chappell
    @author         Matthew Wimberley
    @date           24-Feb-2022
    '''
    
import pyb, utime
from ulab import numpy as np
from math import sin, cos, atan2, pi, acos, asin, atan


## Need to define the universe to z0 reference frame. This will be done using solidworks.
def fwd_kinematics(theta1, theta2, l1, l2, offset):
    '''@brief       derives end effector position and orientation
       @details     Using ME 423 matrices and methods, we found the forward
                    kinematic equations that expresses the final position
                    in terms of the robot arm angles.
       @param       theta1  robot arm 1 angle
       @param       theta2  robot arm 2 angle
       @param       l1      robot arm 1 length
       @param       l2      robot arm 2 length
       @param       offset  arm 2 angular offset from arm 2
       '''
       
    d1 = 0
    d2 = offset
    alpha1 = 0
    alpha2 = 0
    start = utime.ticks_us()
    A1 = np.array([[cos(theta1), -sin(theta1)*cos(alpha1),  sin(theta1)*sin(alpha1), l1*cos(theta1)],
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
    
def inv_kinematics(x, y, l1, l2):
    '''@brief       derives robot arm angles necessary for desired end position
       @details     Using the same analyses from ME 423, we go backwards and
                    start with the end effector position, from here we derive
                    the necessary robot arm angles to give us our desired end
                    position.
       @param       x   End effector x-coordinate
       @param       y   End effector y-coordinate
       @param       l1  robot arm 1 length
       @param       l2  robot arm 2 length
       '''
       
    theta1 = atan2(y/l1, (x-l2)/l1)
    theta2 = acos((x**2 + y**2 + l1 + l2)/(2*l1*l2))
#     theta2 = 0
    theta_1 = atan(x/y) - atan(l2*sin(theta2))/(l1+l2*cos(theta2))
    print(theta_1, theta2)

if __name__ == '__main__':
    fwd_kinematics(pi/2, 0, 6, 3, -4)
#     inv_kinematics(4.2426, 7.2426, 6, 3)