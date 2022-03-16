'''     @file      user_task.py
        @brief     sets up user task
        @details   Originally, the user would get to choose from 4 different 
                   text files that contain the x and y coordinates for the 
                   vector image. Currently, we have one such file.

        @author    Jeremy Baechler
        @author    Kendall Chappell
        @author    Matthew Wimberley
        @date      5-March-2022
'''

def run():
    ''' @brief      runs our user task
        @details    This function asks for user input to select a file with 
                    preprocessed x and y coordinates.
    '''
    
    print('Welcome to the SCARA Robot Laser engraver! Please select the image file you wish to engrave.')
    print('Press "1" for image 1 \r\n Press "2" for image 2 \r\n Press "3" for image 3 \r\n')
    image = int(input('Please Enter Desired Image!:\r\n'))
    if image == 1:
        filename = 'xy.txt'
        
    
    elif image == 2:
        filename = 'file2.txt'
        
    elif image == 3:
        filename = 'file3.txt'
        
    else:
        print('Please enter a valid image number')
          
          
    return filename

