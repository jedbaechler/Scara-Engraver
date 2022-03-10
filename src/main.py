'''
    @file           main.py
    @brief          An adapted main file from basic_tasks.py
    @details        This file contains a demonstration program that runs 
                    some tasks, an inter-task shared variable, and a queue. 
                    The tasks don't really do anything; the example just shows
                    how these elements are created and run. 
                    We added motor control functions that act as the 
                    scheduler.

    @author         Jeremy Baechler
    @author         Kendall Chappell
    @author         Matthew Wimberley
    @date           31-Jan-2022
    '''

import gc
import pyb
import cotask
import task_share
import EncoderReader, controlloop, pyb, utime, x_yimport, user_task, kinematics, homing_script
import motor_baechler_chappell_wimberley as motor_drv

def position_check():
    count = 0
    update_theta1 = 0
    update_theta2 = 0
    while True:
        current_theta1 = enc1.read()
        current_theta2 = enc2.read()
        print('current position:',current_theta1, current_theta2)
        if not count == 0:
            if current_theta1 == previous_theta1 and current_theta2 == previous_theta2:
                print('Setpoint has been hit')
                pinC0.high()
                update_theta1 = list_theta1.get()
                update_theta2 = list_theta2.get()
#                 
#             
        count = 1
        print('Inside position_check')
        theta1.put(update_theta1)
        theta2.put(update_theta2)
        print('Setpoint values', theta1.get(), theta2.get())
#             
        previous_theta1 = current_theta1
        previous_theta2 = current_theta2
        print('leaving position_check')
        yield()
        
    
    
def motor1_func ():
    '''
        @brief      instantiates motor 1 object
        @details    This function reads the encoder data, which the controller
                    uses to find the new PWM, which then sets the new motor
                    speed.

    '''
    while True:
        PWM1 = controller1.run(enc1.read(), theta1.get())
        controller1.add_data()
#           print('Motor 1 Data:', enc1.read(), PWM1)
        mot1.set_duty(PWM1)
        print('Inside motor1 task')
        print('Motor 1 PWM Output', PWM1)
        yield ()
    

def motor2_func():
    '''
        @brief      instantiates motor 2 object
        @details    This function reads the encoder data, which the controller
                    uses to find the new PWM, which then sets the new motor
                    speed.

    '''
    while True:
        PWM2 = controller2.run(enc2.read(), theta2.get())
#         controller2.add_data()
#           print('Motor 2 Data:', enc2.read(), PWM2)
        mot2.set_duty(PWM2)
        print('Motor 2 duty:', PWM2)
        print('Inside motor 2 func')
        yield()


def task2_fun ():
    '''
        @brief      prints data from shares and queues
        @details    Because this is a generator, we only print the data
                    at our discretion.
        '''
        
    while True:
        # Show everything currently in the queue and the value in the share
        print ("Share: {:}, Queue: ".format (share0.get ()), end='');
        while q0.any ():
            print ("{:} ".format (q0.get ()), end='')
        print ('')

        yield (0)


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.

if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')

    # Create a share and a queue to test function and diagnostic printouts
#     share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
#     q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
#                            name = "Queue 0")
    
    xypos = []
    
    theta1 = task_share.Share('f', thread_protect = False, name = "Motor Angle 1")
    theta2 = task_share.Share('f', thread_protect = False, name = "Motor Angle 2")
    
    next_theta1 = task_share.Share('f', thread_protect = False, name = "Subsequent Motor Angle 1")
    next_theta2 = task_share.Share('f', thread_protect = False, name = "Subsequent Motor Angle 2")
    
    list_theta1 = task_share.Queue('f', 100, thread_protect = False, overwrite = False,
                             name = 'theta1-coordinates')
    list_theta2 = task_share.Queue('f', 100, thread_protect = False, overwrite = False,
                             name = 'theta2-coordinates')
    
    next_x = task_share.Queue('f', 100, thread_protect = False, overwrite = False,
                             name = 'x-coordinates')
    next_y = task_share.Queue('f', 100, thread_protect = False, overwrite = False,
                             name = 'y-coordinates')

#     mot1_pos = task_share.Share('h', name='mot1_pos') #shares motor1 position
#     des_pos = task_share.Share('h', name='des_pos') #shares desired position
#     kp = task_share.Share('h', name='kp') #shares kp
#     pwm1 = task_share.Share('h', name='pwm1') #shares motor 1 duty cycle

    """ PLEASE PLUG ENCODER 1 BLUE WIRE INTO B7 AND YELLOW WIRE TO B6"""
    ENA = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP) #motor 1 enabler
    IN1 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP) 
    IN2 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #motor port A pins
    tim3 = pyb.Timer (3, freq=20000) #timer 3 

    """PLEASE PLUG ENCODER 2 BLUE WIRE INTO C7 AND YELLOW WIRE TO C6"""
    ENB = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP) #motor 2 enabler
    IN3 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    IN4 = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP) #motor port B pins
    tim5 = pyb.Timer (5, freq=20000) #using timer 5, must be different than m1

    mot1 = motor_drv.MotorDriver(ENA, IN1, IN2, tim3) #instants motor object
    enc1 = EncoderReader.EncoderReader(1) #instantiates encoder reader object
    #controller1 = controlloop.ClosedLoop(.1, 0.00005, .75, 0) #sets gain and setpoint of m1
    controller1 = controlloop.ClosedLoop(10, 0)

    mot2 = motor_drv.MotorDriver(ENB, IN3, IN4, tim5) #now for motor 1 
    enc2 = EncoderReader.EncoderReader(2) #now for encoder 1
    #controller2 = controlloop.ClosedLoop(.1, 0.00005, 0.75, 0) #sets gain and setpoint of m2
    controller2 = controlloop.ClosedLoop(10, 0)
    
    

    
    pinC2 = pyb.Pin (pyb.Pin.board.PC2, pyb.Pin.IN) # homing limit switch J1
    pinC3 = pyb.Pin (pyb.Pin.board.PC3, pyb.Pin.IN) # homing limit switch J2
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)  # laser on/off
    pinB3 = pyb.Pin(pyb.Pin.board.PB3, pyb.Pin.IN)  # lid open/closed
    
    ''' ISR Definition and Initiation'''
    
    tim1 = pyb.Timer (1, freq=100)



    def ISR_SCREEN(IRQ_src):
        '''
        @brief      sets interrupt every millisecond where ADC value is read
        @details    Once data is collected for one second, "Stop Transmission" line
                    is sent where CTRL-C and CTRL-D commands are sent over serial
                    communication. 
        @param      IRQ_src         The cause of the interrupt
        '''
        
        if pinB3.value() == 1:
#             pinC0.high()
#             print('Lid is closed')
            pass
            
            
        elif pinB3.value() == 0:
            print('Lid is open')
            pinC0.low()
            mot1.disable()
            mot2.disable()
            
        # Set mosfet control pin off for laser
        # turn motors off and halt the operation of tasks
        # move to home position and wait for user to begin program again.
    

    tim1.callback(ISR_SCREEN) # runs when interrupt is called
    
    '''This is the start of our program'''
    
    filename = user_task.run()
 
    coord_values = x_yimport.x_yimport(filename)
 
    x = coord_values[0]
    y = coord_values[1]

    for i in range(len(x)):
        
        constant = 8384/(2*3.1415)*20/110 #radians to ticks
        
        output_kin = kinematics.inv_kinematics(x[i], y[i])
        
        list_theta1.put(constant*output_kin[0])
        list_theta2.put(constant*output_kin[1])
        
#     while True:
#         print(list_theta1.get(), list_theta2.get())
 
    
    homing_script.homing()
    
    mot1.set_duty(0)
    mot2.set_duty(20)
    pinC0.high()
    
#     mot_task1 = cotask.Task (motor1_func, name = 'MotorTask_1', priority = 1, 
#                          period = 10, profile = True, trace = False)
#     mot_task2 = cotask.Task (motor2_func, name = 'MotorTask_2', priority = 1, 
#                            period = 10, profile = True, trace = False)
    pos_checker3 = cotask.Task (position_check, name = 'Position_Checker', priority = 1,
                                period = 5, profile = True, trace = False)
#     
#     mot2.set_duty(-20)  
# 
#     cotask.task_list.append(mot_task1)
#     cotask.task_list.append(mot_task2)

    cotask.task_list.append(pos_checker3)


    
        
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    
#     while not vcp.any ():
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            pinC0.low()
            mot1.set_duty(0)
            mot2.set_duty(0)
            
            break
    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()
    


# Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
#     print (task1.get_trace ())
    print ('\r\n')
