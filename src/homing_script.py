'''     @file      homing_script.py
        @brief     Homes robot
        @details   The robot spins each axis one at a time until the limit
                   switch is hit. This physical contact on the first arm 
                   disables the motor then spins the second arm until it has
                   reached its respective limit switch.

        @author    Jeremy Baechler
        @author    Kendall Chappell
        @author    Matthew Wimberley
        @date      5-March-2022
'''

import pyb, utime
import motor_baechler_chappell_wimberley as motor_drv
import EncoderReader

pinC3 = pyb.Pin (pyb.Pin.board.PC3, pyb.Pin.IN)
pinC2 = pyb.Pin (pyb.Pin.board.PC2, pyb.Pin.IN)

enc1 = EncoderReader.EncoderReader(1)
enc2 = EncoderReader.EncoderReader(2)

ENA = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP) #motor 1 enabler
IN1 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP) 
IN2 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #motor port A pins
tim3 = pyb.Timer (3, freq=20000) #timer 3 

ENB = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP) #motor 2 enabler
IN3 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
IN4 = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP) #motor port B pins
tim5 = pyb.Timer (5, freq=20000) #using timer 5, must be different than m1

mot1 = motor_drv.MotorDriver(ENA, IN1, IN2, tim3)
mot2 = motor_drv.MotorDriver(ENB, IN3, IN4, tim5)

mot1.set_duty(25)
mot2.set_duty(-25)
limit_trigger1 = 0
limit_trigger2 = 0

'''@details     The above is all tester code for setting up the necessary robot
                positions for the homing function to work properly. Notably, 
                arm angle 1 must be less than arm 1 angle desired so that the
                cables to not tangle.
                '''

def homing():
    ''' @brief       homes robot from which our inverse kinematics are with respect to
        @details     This function moves one robot arm at a time until the limit
                     switch is reached, thus breaking out of the loop 
                     and activating the second motor arm. Once the home is reached,
                     confirmation statements are printed to the screen.
                     '''
    
    mot2.set_duty(-25)
    limit_trigger1 = 0
    limit_trigger2 = 0
    
    while True:
        if pinC3.value() == 1:
            print('Arm 2 has reached its hardstop')
            enc2.zero()
            mot2.disable()
            limit_trigger1 = 1
            break
            
        else:
    #         print('Moving arm 1 to homing location')
            pass
        
    mot1.set_duty(25)
    
    while True:
        if pinC2.value() == 1:
            print('Arm 1 has reached its hardstop')
            enc1.zero()
            mot1.disable()
            limit_trigger2 = 1
            break
        
        else:
    #         print('Moving Arm 2 to home location')
            pass
        
    print('Zero positions have been reached!')
        
    print(enc1.read(), enc2.read())
    
