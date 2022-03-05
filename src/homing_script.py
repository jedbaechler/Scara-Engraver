'''
@file homing_script.py
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

while True:
    
    if pinC3.value() == 1:
        print('Arm 1 has reached its hardstop')
        enc1.zero()
        mot1.disable()
        limit_trigger1 = 1
        
    else:
#         print('Moving arm 1 to homing location')
        pass

    if pinC2.value() == 1:
        print('Arm 2 has reached its hardstop')
        enc2.zero()
        mot2.disable()
        limit_trigger2 = 1
    else:
#         print('Moving Arm 2 to home location')
        pass
    if limit_trigger1 == 1 and limit_trigger2 == 1:
        print('Zero positions have been reached')
        break
    
print(enc1.read(), enc2.read())
    
