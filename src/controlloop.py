''' @file       controlloop.py
    @brief      sets up closed loop motor control
    @details    After setpoint and K_p gain values are set by user, 
                the controller continuously checks the encoder values to 
                minimize the setpoint error. However, there is always a steady
                state error due to there being no integrator in the control 
                loop.
                
    @author     Jeremy Baechler
    @author     Kendall Chappell
    @author     Matthew Wimberley
    @date       31-Jan-2022

'''

import utime, EncoderReader
from ulab import numpy as np

class ClosedLoop:
    '''@brief   Closed Loop Control System
       @details This class contains useful functions we need for the 
                controller to be effective at getting to the motor setpoint.
       '''
    
    def __init__(self, Kp, Ki, Kd, ref):
        '''@brief   takes in gain value and setpoint
           @details This instantiates necessary objects to capture
                    controller's values.
           @param   Kp      gain value
           @param   ref     reference point
           '''
           
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.ref = ref
        self.listpos = []
        self.time = []
        self.start_time = utime.ticks_ms()
        self.enc1 = EncoderReader.EncoderReader(1)
        self.old_pos = 0
        self.old_time = utime.ticks_us()
        self.error = np.array([0]*1000)
        self.i = 0
        self.integral = 0
        self.deriv = 0
    
    def run(self, pos, ref):
        '''@brief   runs the proportional control loop
           @details Only acting as a P-controller, this function multiplies
                    our gain by the difference between the reference point
                    and the current position.
           @param   pos     current position
           '''
           
        self.pos = pos
        self.ref = ref
        self.error[i] = self.ref-self.pos
        self.new_time = utime.ticks_us()
        self.new_pos = self.enc1.read()
        self.time_diff = utime.ticks_diff(self.new_time, self.old_time)
        self.deriv = self.error[i]/self.time_diff
        self.integral += self.error[self.i]*self.time_diff
        duty = self.error * self.Kp + self.deriv * self.Kd + self.integral * self.Ki
        self.old_pos = self.new_pos
        self.old_time = utime.ticks_us()
        self.i += 1
        return duty
        
    
    def set_ref(self, ref):
        '''@brief   sets reference point
           @param   ref     set point
           '''
           
        self.ref = ref
    
    def set_Kp(self, Kp):
        '''@brief   sets proportional gain value
           @param   Kp  gain value
           '''
           
        self.Kp = Kp
    
    def add_data(self):
        '''@brief   makes list of position and time
           @details Time is gathered as column 1 while column 2 is encoder
                    position. Plotting these two together gives a nice
                    step response.
            '''
            
        self.current_time = utime.ticks_ms()
        time = utime.ticks_diff(self.current_time, self.start_time)
        self.time.append(time)
        self.listpos.append(self.pos)
    
    

if __name__ == '__main__':
    '''@brief   test code for closed loop controller
    '''
    
    controller = ClosedLoop(.15, 10)
    print(controller.run(5))
