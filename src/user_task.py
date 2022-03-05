'''
@file      user_task.py
@brief     sets up user task
@details   

@author    Jeremy Baechler
@author    Kendall Chappell
@author    Matthew Wimberley
@date      5-March-2022
'''

print('Welcome to the SCARA Robot Laser engraver! Please select the image file you wish to engrave.')

print('Press "1" for image 1 \r\n Press "2" for image 2 \r\n Press "3" for image 3 \r\n')

def run():
    if input == 1:
        filename = 'xy.txt'
        
    
    elif input == 2:
        filename = 'file2.txt'
        
    elif input == 3:
        filename = 'file3.txt'
        
    else:
        print('Please enter a valid image number')
          
          
    return filename

