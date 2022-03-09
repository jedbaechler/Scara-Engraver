'''
@file      EncoderReader.py
@brief     sets up encoder to be able to read values past 65535
@details   holds onto last value at each read, so negative values 
           and very large values can be stored and read with no hard limit 

@author    Jeremy Baechler
@author    Kendall Chappell
@author    Matthew Wimberley
@date      20-Jan-2022
'''

import pyb, utime

class EncoderReader:


    '''@brief       sets up class encoder to be used locally by other programs
       @details     saves last value of each cycle to be added or subtracted
       '''
       
    

    def __init__(self, enc_number):
        '''@brief      instantiates encoder objects
           @details    we know the encoder pins, so user can just select encoders
           '''
        self.current_position = 0
        self.delta = 0
        self.enc_number = enc_number

        
        if enc_number == 1:
            '''@brief   sets up first encoder'''
            
            self.timer = pyb.Timer(4, prescaler = 0, period = 65535)
            self.ch1 = self.timer.channel(1, pyb.Timer.ENC_AB, pin = pyb.Pin.cpu.B6)
            self.ch2 = self.timer.channel(2, pyb.Timer.ENC_AB, pin = pyb.Pin.cpu.B7)
            
        elif enc_number ==2:
            '''@brief   sets up second encoder'''
        
            self.timer = pyb.Timer(8, prescaler = 0, period = 65535)
            self.ch1 = self.timer.channel(1, pyb.Timer.ENC_AB, pin = pyb.Pin.cpu.C6)
            self.ch2 = self.timer.channel(2, pyb.Timer.ENC_AB, pin = pyb.Pin.cpu.C7)  

    def read(self):

        
        '''@brief       needs at least 2 values in each period
           @details     if >=2 values then delta can be accurately recorded
                        saved and then subtracted from last known value
           @returns     current encoder position'''
                        

        previous_position = self.current_position % 65535
        self.delta = self.timer.counter() - previous_position

        if self.delta < -65535/2:
            self.delta += 65535
        elif self.delta > 65535/2:
            self.delta -= 65535
        self.current_position += self.delta
        
        return self.current_position
        
    def zero(self):
        '''@brief       zeroes encoder position
        '''
        
        self.current_position = 0
        self.delta = 0
        
        if self.enc_number == 1:
            self.timer = pyb.Timer(4, prescaler = 0, period = 65535)
        if self.enc_number == 2:
            self.timer = pyb.Timer(8, prescaler = 0, period = 65535)
        
if __name__ == "__main__":
    '''@brief    testing block for encoder-motor pair
    '''
    
    import motor_baechler_chappell_wimberley as motor_drv
    
    ENA = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OPEN_DRAIN, pull=pyb.Pin.PULL_UP)
    IN1 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    IN2 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    tim3 = pyb.Timer (3, freq=20000)
    mot1 = motor_drv.MotorDriver(ENA, IN1, IN2, tim3)

    ENB = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP) #motor 2 enabler
    IN3 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    IN4 = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP) #motor port B pins
    tim5 = pyb.Timer (5, freq=20000) #using timer 5, must be different than m1
    mot2 = motor_drv.MotorDriver(ENB, IN3, IN4, tim5) #now for motor 1 
    
    
    mot1.set_duty(0)
    mot2.set_duty(20)
