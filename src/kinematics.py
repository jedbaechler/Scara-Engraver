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
       
    h1 = 8
    l2_reset = offset
    alpha1 = 0
    alpha2 = 0
    h2 = 4
    start = utime.ticks_us()
    
    A1 = np.array([[cos(theta1), -sin(theta1),  0, 0],
                   [sin(theta1), cos(theta1), 0, 0],
                   [0, 0, 1, h1],
                   [0, 0, 0, 1]])
    
    A1Jeremy = np.array([[cos(theta1), -sin(theta1)*cos(alpha1),  sin(theta1)*sin(alpha1), 0],
                   [sin(theta1), cos(theta1)*cos(alpha1), -cos(theta1)*sin(alpha1), 0],
                   [0, sin(alpha1), cos(alpha1), h1],
                   [0, 0, 0, 1]])
    
    A2 = np.array([[1, 0, 0, l1],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    A3 = np.array([[cos(theta2-l2_reset), -sin(theta2-l2_reset), 0, l2*cos(theta2-l2_reset)],
                   [sin(theta2-l2_reset), cos(theta2-l2_reset), 0, l2*sin(theta2-l2_reset)],
                   [0, 0, 1, -h2],
                   [0, 0, 0, 1]])
    
    A2Jeremy = np.array([[cos(theta2), -sin(theta2)*cos(alpha2), sin(theta2)*sin(alpha2), l2*cos(theta2)],
                   [sin(theta2), cos(theta2)*cos(alpha2), -cos(theta2)*sin(alpha2), l2*sin(theta2)],
                   [0, sin(alpha2), cos(alpha2), -h2],
                   [0, 0, 0, 1]])
    
    A12 = np.dot(A1,A2)
    A123 = np.dot(A12, A3)
    A12J = np.dot(A1Jeremy, A2Jeremy)
    P = np.array([[0],[0],[3],[1]])
    end_effector = np.dot(A123, P)
    print('matt:' + str(A123))
    print('Jeremy:' + str(A12J))


    
    #fwd kinematics end effectors must be adjusted
    
def inv_kinematics(x, y):
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
       
       # l1 = 8 in
       # l2 = 4 in

    theta_1_first = 2*atan((16*y - (144*(-(x**2 + y**2 - 16)*(x**2 + y**2 - 144))**(1/2))/(x**2 + y**2 - 144) + (x**2*(-(x**2 + y**2 - 16)*(x**2 + y**2 - 144))**(1/2))/(x**2 + y**2 - 144) + (y**2*(-(x**2 + y**2 - 16)*(x**2 + y**2 - 144))**(1/2))/(x**2 + y**2 - 144))/(x**2 + 16*x + y**2 + 48))
        
    theta_2_first = -2*atan((-(x**2 + y**2 - 16)*(x**2 + y**2 - 144))**(1/2)/(x**2 + y**2 - 144))


    theta_1_second = 2*atan((16*y + (144*(-(x**2 + y**2 - 16)*(x**2 + y**2 - 144))**(1/2))/(x**2 + y**2 - 144) - (x**2*(-(x**2 + y**2 - 16)*(x**2 + y**2 - 144))**(1/2))/(x**2 + y**2 - 144) - (y**2*(-(x**2 + y**2 - 16)*(x**2 + y**2 - 144))**(1/2))/(x**2 + y**2 - 144))/(x**2 + 16*x + y**2 + 48))

    theta_2_second = 2*atan((-(x**2 + y**2 - 16)*(x**2 + y**2 - 144))**(1/2)/(x**2 + y**2 - 144))

    return (theta_1_first, theta_2_first)

# x^2 + y^2 <= 8
# x^2 + y^2 >= 4


if __name__ == '__main__':
    print(fwd_kinematics(1.272, 0.7227, 8, 4, 1.57))
    print(inv_kinematics(4,4))