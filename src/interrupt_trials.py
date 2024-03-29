'''
    @file           main.py
    @brief          Reads ADC pin on Nucleo and saves data in queue
    @details        This file instantiates the output and analog read out pins.
                    The ADC pin value is read every millisecond then the 
                    corresponding data entry gets added to the queue. 

    @author         Jeremy Baechler
    @author         Kendall Chappell
    @author         Matthew Wimberley
    @date           16-Feb-2022
    '''
    
import pyb, utime, task_share
import micropython
import motor_baechler_chappell_wimberley as motor_drv
micropython.alloc_emergency_exception_buf(100)


pinPC1 = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.IN)
tim1 = pyb.Timer (1, freq=100)
pinPB0 = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.OUT_PP)



def ISR_SCREEN(IRQ_src):
    '''
    @brief      sets interrupt every millisecond where ADC value is read
    @details    Once data is collected for one second, "Stop Transmission" line
                is sent where CTRL-C and CTRL-D commands are sent over serial
                communication. 
    @param      IRQ_src         The cause of the interrupt
    '''
    
    if pinPC1.value() == 1:
        print('Lid is closed')
        
    elif pinPC1.value() == 0:
        print('Lid is open')
        
        # Set mosfet control pin off for laser
        pinPB0.low()
        # turn motors off and halt the operation of tasks
        motor_drv.disable()


tim1.callback(ISR_SCREEN) # runs when interrupt is called
    

# We used this to test runs on first order response.
        
# while True: 

#     pinPC1.low()
#     utime.sleep_ms(2000)
#     pinPC1.high()
#     utime.sleep_ms(2000)

